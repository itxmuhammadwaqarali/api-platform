from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from fastapi.responses import JSONResponse
from app.core.redis_client import redis_client
from asgiref.sync import sync_to_async
import asyncio
from app.core.webhooks import get_webhooks_for_event
from app.core.webhook_utils import trigger_webhook
from app.core.config import APIKey

# Public paths that don't require API key
PUBLIC_PATHS = ["/docs", "/openapi.json", "/redoc", "/favicon.ico"]

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, limit: int = 5, window: int = 60):
        super().__init__(app)
        self.limit = limit
        self.window = window

    async def dispatch(self, request: Request, call_next):
        # Skip rate limiting for public/documentation endpoints
        if any(request.url.path.startswith(path) for path in PUBLIC_PATHS):
            response = await call_next(request)
            return response

        api_key = request.headers.get("x-api-key") or request.query_params.get("api_key")
        if not api_key:
            return JSONResponse(status_code=400, content={"detail": "API key missing"})

        # Get API key and plan from database
        try:
            key_obj = await sync_to_async(APIKey.objects.select_related('plan').get)(key=api_key, active=True)
        except APIKey.DoesNotExist:
            return JSONResponse(status_code=401, content={"detail": "Invalid API Key"})

        # Get plan limits, fallback to default if no plan
        if key_obj.plan and key_obj.plan.active:
            limit = key_obj.plan.requests_per_minute
        else:
            # Default limits for keys without plans (free tier)
            limit = 10  # Very restrictive for unassigned keys

        key = f"rate:{api_key}"

        try:
            # Async-safe Redis get
            current = await asyncio.to_thread(redis_client.get, key)

            if current is None:
                # First request: set counter with expiry
                await asyncio.to_thread(redis_client.set, key, 1, ex=60)  # 1 minute window
            elif int(current) >= limit:
                # Trigger webhooks asynchronously
                webhooks = get_webhooks_for_event("rate_limit_exceeded", api_key)
                for wh in webhooks:
                    asyncio.create_task(trigger_webhook(wh, {
                        "api_key": api_key,
                        "path": str(request.url),
                        "limit": limit,
                        "window": 60,
                        "method": request.method,
                        "plan": key_obj.plan.name if key_obj.plan else "none"
                    }))
                return JSONResponse(status_code=429, content={"detail": f"Rate limit exceeded. Plan limit: {limit} requests per minute"})
            else:
                # Increment counter
                await asyncio.to_thread(redis_client.incr, key)

        except Exception as e:
            return JSONResponse(status_code=500, content={"detail": f"Rate limiter error: {str(e)}"})

        response = await call_next(request)
        return response