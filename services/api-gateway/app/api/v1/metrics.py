from fastapi import APIRouter, Request, HTTPException
from app.core.redis_client import redis_client
import asyncio

router = APIRouter()

@router.get("/metrics")
async def get_metrics(api_key: str):
    if not api_key:
        raise HTTPException(status_code=400, detail="API key is required")

    # Fetch usage from Redis asynchronously
    usage_keys = await asyncio.to_thread(redis_client.keys, f"usage:{api_key}:*")
    usage = {}
    for key in usage_keys:
        count = await asyncio.to_thread(redis_client.get, key)
        usage[key.decode().split(":")[-1]] = int(count)

    return {"api_key": api_key, "usage": usage}