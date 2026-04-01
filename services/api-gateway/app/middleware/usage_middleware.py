from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from app.core.redis_client import redis_client
import asyncio

class UsageMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        api_key = request.headers.get("X-API-Key")
        if api_key:
            key = f"usage:{api_key}:{request.url.path}"
            await asyncio.to_thread(redis_client.incr, key)
        response = await call_next(request)
        return response