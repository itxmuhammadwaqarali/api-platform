from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from asgiref.sync import sync_to_async
from app.core.config import APIKey  # Django model import

class APIKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        if request.url.path.startswith("/v1") or request.url.path == "/test-key":
            api_key = request.headers.get("x-api-key")

            # Check Django DB for active key
            if not api_key or not await sync_to_async(APIKey.objects.filter(key=api_key, active=True).exists)():
                return JSONResponse(
                    status_code=401,
                    content={"detail": "Invalid API Key"}
                )

        response = await call_next(request)
        return response