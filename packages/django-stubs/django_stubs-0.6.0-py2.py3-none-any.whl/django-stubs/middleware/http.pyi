from django.core.handlers.wsgi import WSGIRequest
from django.http.response import HttpResponseBase
from django.utils.deprecation import MiddlewareMixin

class ConditionalGetMiddleware(MiddlewareMixin):
    def process_response(self, request: WSGIRequest, response: HttpResponseBase) -> HttpResponseBase: ...
    def needs_etag(self, response: HttpResponseBase) -> bool: ...
