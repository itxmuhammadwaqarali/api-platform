# app/middleware/rate_limit_middleware.py
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from app.core.redis_client import redis_client  # Use aioredis or sync redis for blocking

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
            # Get current request count
            current = redis_client.get(key)
            if current is None:
                # First request → set counter with expiry
                redis_client.set(key, 1, ex=self.window)
            elif int(current) >= self.limit:
                # Rate limit exceeded
                return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded"})
            else:
                # Increment counter
                redis_client.incr(key)

        except Exception as e:
            # Redis connection error fallback
            return JSONResponse(status_code=500, content={"detail": f"Rate limiter error: {str(e)}"})

        # Proceed to next middleware or route
        response = await call_next(request)
        return response