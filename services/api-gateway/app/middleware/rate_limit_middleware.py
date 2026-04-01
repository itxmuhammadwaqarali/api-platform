# app/middleware/rate_limit_middleware.py
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from fastapi.responses import JSONResponse
from app.core.redis_client import redis_client
from asgiref.sync import sync_to_async
import asyncio
from app.core.webhooks import get_webhooks_for_event
from app.core.webhook_utils import trigger_webhook

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, limit: int = 5, window: int = 60):
        super().__init__(app)
        self.limit = limit
        self.window = window

    async def dispatch(self, request: Request, call_next):
        api_key = request.headers.get("X-API-Key")
        if not api_key:
            return JSONResponse(status_code=400, content={"detail": "X-API-Key header missing"})

        key = f"rate:{api_key}"

        try:
            # Async-safe Redis get
            current = await asyncio.to_thread(redis_client.get, key)

            if current is None:
                # First request: set counter with expiry
                await asyncio.to_thread(redis_client.set, key, 1, ex=self.window)
            elif int(current) >= self.limit:
                # Trigger webhooks asynchronously
                webhooks = await sync_to_async(get_webhooks_for_event)("rate_limit_exceeded")
                for wh in webhooks:
                    asyncio.create_task(trigger_webhook(wh, {
                        "api_key": api_key,
                        "path": str(request.url),
                        "limit": self.limit,
                        "window": self.window,
                        "method": request.method
                    }))
                return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded"})
            else:
                # Increment counter
                await asyncio.to_thread(redis_client.incr, key)

        except Exception as e:
            return JSONResponse(status_code=500, content={"detail": f"Rate limiter error: {str(e)}"})

        response = await call_next(request)
        return response