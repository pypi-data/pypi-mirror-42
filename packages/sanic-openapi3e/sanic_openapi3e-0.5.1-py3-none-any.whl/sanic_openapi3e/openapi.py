"""
Build the OpenAPI spec.

Note: ```app.config.HIDE_OPENAPI_SELF``` is used to hide the ``/openapi`` and ``/swagger`` paths from the spec. The
      default value is `True`. To reveal these endpoints in the spec, set it explicitly to `False`.

Known limitations:
* Parameters are documented at the PathItem level, not at the underlying Operation level.

"""
import re
from typing import Dict
from itertools import repeat
from collections import OrderedDict

# from loguru import logger
import sanic
import sanic.response
import sanic.exceptions
from sanic.blueprints import Blueprint
from sanic.views import CompositionView

from .oas_types import (
    Info,
    Parameter,
    OpenAPIv3,
    Operation,
    PathItem,
    Paths,
    Response,
    Responses,
)
from .doc import paths, tags, Schema
from .swagger import blueprint as swagger_bp

blueprint = Blueprint("openapi", url_prefix="openapi")

NotYetImplemented = None
NotYetImplementedResponses = Responses(
    {"200": Response(description="A successful response")}
)


_openapi = {}
"""
Module-level container to hold the OAS spec that will be served-up on request. See `build_openapi_spec` for how it is
built.
"""

_openapi_all = {}
"""
Module-level container to hold the OAS spec that may be served-up on request. The difference with this one is that it 
contains all paths, including those marked as `exclude`.
"""

CAST_2_SCHEMA = {
    type(1): Schema.Integer,
    type(1.1): Schema.Number,
    type("1"): Schema.String,
}


@blueprint.listener("before_server_start")
def build_openapi_spec(app, _):
    hide_openapi_self = app.config.get("HIDE_OPENAPI_SELF", True)
    show_excluded = app.config.get("SHOW_OPENAPI_EXCLUDED", False)
    # logger.warning("Setting show_excluded")
    # show_excluded = True

    openapi = _build_openapi_spec(app, hide_openapi_self, hide_excluded=True)
    global _openapi
    _openapi = openapi.serialize()

    if show_excluded:
        openapi_all = _build_openapi_spec(app, hide_openapi_self, hide_excluded=False)
        global _openapi_all
        _openapi_all = openapi_all.serialize()


def _build_openapi_spec(app, hide_openapi_self=True, hide_excluded=True):
    """
    Build the OpenAPI spec.

    :param app:
    :param hide_openapi_self:
    :param hide_excluded:
    :return: The spec
    :type app: sanic.Sanic
    :type hide_openapi_self: bool
    :type hide_excluded: bool
    :rtype OpenAPIv3
    """

    _oas_paths = OrderedDict()
    for _uri, _route in app.router.routes_all.items():
        if hide_openapi_self:
            if (
                _uri.startswith("/" + blueprint.url_prefix)
                if blueprint.url_prefix
                else True
            ) and any([bp_uri in _uri for bp_uri in [r.uri for r in blueprint.routes]]):
                # Remove self-documentation from the spec
                continue
            if (
                _uri.startswith("/" + swagger_bp.url_prefix)
                if swagger_bp.url_prefix
                else True
            ) and any(
                [bp_uri in _uri for bp_uri in [r.uri for r in swagger_bp.routes]]
                + [not bool(swagger_bp.routes)]
            ):
                # Remove self-documentation from the spec
                continue

        # We will document the parameters at the PathItem, not at the Operation. First get the route parameters (if any)
        uri_parsed = _uri
        parameters = dict()  # type: Dict[str, Parameter]
        for _parameter in _route.parameters:
            uri_parsed = re.sub(
                "<" + _parameter.name + ".*?>", "{" + _parameter.name + "}", uri_parsed
            )

            parameter = Parameter(
                name=_parameter.name,
                _in="path",
                description=None,
                required=True,
                deprecated=None,
                allow_empty_value=None,
                style=None,
                explode=None,
                allow_reserved=None,
                schema=CAST_2_SCHEMA.get(_parameter.cast),
                example=None,
                examples=None,
                content=None,
            )

            parameters[_parameter.name] = parameter

        handler_type = type(_route.handler)
        if handler_type is CompositionView:
            view = _route.handler
            pathitem_operations = view.handlers.items()
        else:
            pathitem_operations = zip(_route.methods, repeat(_route.handler))

        operations = OrderedDict()
        for _method, _func in pathitem_operations:
            path_item = paths[_func]  # type: PathItem
            if path_item.x_exclude and hide_excluded:
                continue

            _parameters = path_item.parameters
            for _parameter in _parameters:
                if _parameter.name in parameters.keys():
                    # Merge them. Parameter has a special __add__ for this.
                    parameters[_parameter.name] = (
                        parameters[_parameter.name] + _parameter
                    )
                else:
                    parameters[_parameter.name] = _parameter

            operations[_method.lower()] = Operation(
                **{
                    "operation_id": "{}::{}".format(_func.__module__, _func.__name__),
                    "summary": path_item.summary,
                    "description": path_item.description,
                    "parameters": set(parameters.values()),
                    "tags": [
                        t.name for t in path_item.x_tags_holder
                    ],  # TODO - list not set to preserve order.
                    "deprecated": path_item.x_deprecated_holder,
                    "responses": path_item.x_responses_holder,
                }
            )

        path = PathItem(**operations, servers=NotYetImplemented)
        _oas_paths[uri_parsed] = path
    info = Info(
        title=getattr(app.config, "API_TITLE", "API"),
        description=getattr(app.config, "API_DESCRIPTION", "Description"),
        terms_of_service=NotYetImplemented,
        contact=NotYetImplemented,
        _license=NotYetImplemented,
        version=getattr(app.config, "API_VERSION", "1.0.0"),
    )

    _v3_paths = Paths(_oas_paths)
    _v3_tags = set(tags.values())
    openapi = OpenAPIv3(
        openapi=OpenAPIv3.version,
        info=info,
        servers=NotYetImplemented,
        paths=_v3_paths,
        components=NotYetImplemented,
        security=NotYetImplemented,
        tags=_v3_tags,
        external_docs=NotYetImplemented,
    )
    return openapi


@blueprint.route("/spec.json")
def spec_v3(_):
    return sanic.response.json(_openapi)


@blueprint.route("/spec.all.json")
def spec_all(_):
    if _openapi_all:
        return sanic.response.json(_openapi_all)
    else:
        raise sanic.exceptions.NotFound()
