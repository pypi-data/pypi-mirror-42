"""
    drf-common-exceptions/exceptions.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Implementation of common exception handler for Django REST framework.

    :copyright: (c) 2019 by Andrey Bogoyavlensky.
"""
import collections
import sys
from collections import OrderedDict
from typing import List, Optional, Union

from rest_framework import exceptions, status
from rest_framework.compat import View
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.settings import api_settings
from rest_framework.views import exception_handler as origin_exception_handler

# TODO: make configurable from settings
DRF_EXCEPTIONS_NON_FIELD_ERRORS_LABEL = None
DRF_EXCEPTIONS_SEPARATOR = "."


def get_service(view: View) -> str:
    """Returns service name by view and stacktrace."""
    service = ".".join([view.__class__.__module__, view.__class__.__name__])
    _, _, tb = sys.exc_info()
    tb = getattr(tb, "tb_next", tb)
    lineno = getattr(tb, "tb_lineno", "")
    return ":".join([service, str(lineno)])


def get_label(path: List[str], serializer: Serializer) -> Optional[str]:
    """Return label for field by serializer data."""
    if not serializer:
        return DRF_EXCEPTIONS_NON_FIELD_ERRORS_LABEL
    field_name, tail = path[0], path[1:]
    if field_name == api_settings.NON_FIELD_ERRORS_KEY:
        return DRF_EXCEPTIONS_NON_FIELD_ERRORS_LABEL
    field = serializer.fields.get(field_name)
    if isinstance(field, Serializer) and tail:
        return get_label(tail, field)
    return getattr(field, "label", "")


def flatten_dict(
    data: collections.MutableMapping,
    parent_key: str = "",
    sep: Optional[str] = None,
) -> dict:
    """Return nested dict as single level dict."""
    sep = sep or DRF_EXCEPTIONS_SEPARATOR
    items: list = []
    for k, v in data.items():
        new_key = sep.join([parent_key, k]) if parent_key and sep else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def handle_errors(value: Union[List[str], str]) -> List[str]:
    """Return list error messages from value."""
    errors = value if isinstance(value, list) else [value]
    return [str(e) for e in errors]


def common_exception_handler(exc: APIException, context: dict) -> Response:
    """Add single format for exception and validation errors.
    Example error:
        {
            "service": "apps.users.viewsets.UserViewSet:20",
            "error": "ValidationError",
            "detail": [
                {
                    "label": "Name",
                    "field": "name",
                    "messages": [
                        "This is required field."
                    ]
                }
            ]
        }
    """
    response = origin_exception_handler(exc, context)
    if response is not None:
        # Detail
        if isinstance(response.data, dict) and "detail" in response.data:
            detail = response.data.get("detail")
        else:
            detail = response.data

        if isinstance(detail, dict):
            serializer = getattr(exc.detail, "serializer", None)
            detail = [
                {
                    "label": get_label(k.split("."), serializer),
                    "field": k,
                    "messages": handle_errors(v),
                }
                for k, v in flatten_dict(detail).items()
            ]
        else:
            messages = detail if isinstance(detail, list) else [detail]
            detail = [
                {
                    "label": DRF_EXCEPTIONS_NON_FIELD_ERRORS_LABEL,
                    "field": api_settings.NON_FIELD_ERRORS_KEY,
                    "messages": messages,
                }
            ]
        # Result
        response.data = OrderedDict(
            [
                ("service", get_service(context.get("view"))),
                ("error", exc.__class__.__name__),
                ("detail", detail),
            ]
        )
    return response


class CommonExceptionHandlerMixin(object):
    """Mixin to apply common exception for particular view."""

    def get_exception_handler(self) -> Response:
        """Return customized exception handler."""
        return common_exception_handler

    def handle_exception(self, exc: APIException) -> Response:
        """Overriding default exception handler for particular views."""
        if isinstance(
            exc, (exceptions.NotAuthenticated, exceptions.AuthenticationFailed)
        ):
            # WWW-Authenticate header for 401 responses, else coerce to 403
            auth_header = self.get_authenticate_header(  # type: ignore
                self.request  # type: ignore
            )
            if auth_header:
                exc.auth_header = auth_header
            else:
                exc.status_code = status.HTTP_403_FORBIDDEN
        exception_handler = self.get_exception_handler()
        context = self.get_exception_handler_context()  # type: ignore
        response = exception_handler(exc, context)
        if response is None:
            self.raise_uncaught_exception(exc)  # type: ignore
        response.exception = True
        return response
