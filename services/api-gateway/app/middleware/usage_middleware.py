from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from app.core.django_setup import django
from usage.utils import log_api_usage  # import your Django logging function

class UsageMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        api_key = request.headers.get("X-API-Key")
        if api_key:
            try:
                log_api_usage(api_key, request.url.path, request.method)
            except Exception as e:
                print(f"Usage logging error: {e}")
        response = await call_next(request)
        return response