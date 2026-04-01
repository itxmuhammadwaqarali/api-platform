from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

VALID_API_KEYS = {"test_key_123"}

class APIKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        if request.url.path.startswith("/v1"):
            api_key = request.headers.get("x-api-key")

            if not api_key or api_key not in VALID_API_KEYS:
                return JSONResponse(
                    status_code=401,
                    content={"detail": "Invalid API Key"}
                )

        response = await call_next(request)
        return response