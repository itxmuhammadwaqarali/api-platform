# services/api-gateway/app/main.py
import sys
import os
import asyncio
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

# Add current folder to path for Django integration
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import middleware
from app.middleware.api_key_middleware import APIKeyMiddleware
from app.middleware.rate_limit_middleware import RateLimitMiddleware
from app.api.v1.router import router as v1_router

# Import usage metrics
from app.core.usage_logger import log_usage  # async-safe logger

app = FastAPI(title="API Platform Gateway")

# Add middleware
app.add_middleware(APIKeyMiddleware)
app.add_middleware(RateLimitMiddleware, limit=5, window=60)

# Include API router
app.include_router(v1_router, prefix="/v1")


@app.middleware("http")
async def usage_logger_middleware(request: Request, call_next):
    """
    Log usage for metrics. Wrap in try/catch to avoid blocking request.
    """
    response = await call_next(request)
    api_key = request.headers.get("X-API-Key")
    if api_key:
        asyncio.create_task(log_usage(api_key, request.url.path, request.method))
    return response


@app.get("/test-key")
def test_key():
    """Simple API key test"""
    return {"message": "API Key validated"}


@app.get("/metrics")
async def metrics():
    """
    Returns simple metrics for all API keys (usage counts)
    """
    from app.core.redis_client import redis_client
    try:
        keys = await asyncio.to_thread(redis_client.keys, "rate:*")
        data = {}
        for k in keys:
            count = await asyncio.to_thread(redis_client.get, k)
            data[k.replace("rate:", "")] = int(count)
        return data
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": f"Metrics error: {str(e)}"})