from typing import Any

from django.core.handlers.wsgi import WSGIRequest
from django.http.response import HttpResponseBase
from django.utils.deprecation import MiddlewareMixin

class LocaleMiddleware(MiddlewareMixin):
    response_redirect_class: Any = ...
    def process_request(self, request: WSGIRequest) -> None: ...
    def process_response(self, request: WSGIRequest, response: HttpResponseBase) -> HttpResponseBase: ...
