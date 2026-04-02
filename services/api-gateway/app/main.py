import sys
import os
import asyncio
from fastapi import FastAPI, Request, Header
from fastapi.responses import JSONResponse
from app.api.v1.metrics import router as metrics_router
from asgiref.sync import sync_to_async


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
app.include_router(metrics_router, prefix="/v1")

# Include API router
app.include_router(v1_router, prefix="/v1")


@app.middleware("http")
async def usage_logger_middleware(request: Request, call_next):
    """
    Log usage for metrics. Wrap in try/catch to avoid blocking request.
    """
    response = await call_next(request)
    api_key = request.headers.get("x-api-key")
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


@app.get("/plan-info")
async def get_plan_info(x_api_key: str = Header(...)):
    """
    Get information about the current API key's plan
    """
    from app.core.config import APIKey

    try:
        key_obj = await sync_to_async(APIKey.objects.select_related('plan').get)(key=x_api_key, active=True)

        if key_obj.plan:
            plan_info = {
                "plan_name": key_obj.plan.name,
                "display_name": key_obj.plan.display_name,
                "requests_per_minute": key_obj.plan.requests_per_minute,
                "requests_per_hour": key_obj.plan.requests_per_hour,
                "requests_per_day": key_obj.plan.requests_per_day,
                "webhook_support": key_obj.plan.webhook_support,
                "priority_support": key_obj.plan.priority_support,
                "custom_rate_limits": key_obj.plan.custom_rate_limits,
            }
        else:
            plan_info = {
                "plan_name": "none",
                "display_name": "No Plan",
                "requests_per_minute": 10,  # Default restrictive limit
                "requests_per_hour": 100,
                "requests_per_day": 1000,
                "webhook_support": False,
                "priority_support": False,
                "custom_rate_limits": False,
            }

        return {
            "api_key": x_api_key,
            "plan": plan_info
        }
    except APIKey.DoesNotExist:
        return JSONResponse(status_code=401, content={"detail": "Invalid API Key"})
