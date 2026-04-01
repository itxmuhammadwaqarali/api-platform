from fastapi import APIRouter, Header, HTTPException
from app.core.redis_client import redis_client
import asyncio

router = APIRouter()

@router.get("/health")
def health_check():
    return {"message": "API Gateway v1 running"}



router = APIRouter()

@router.get("/usage")
async def get_usage(x_api_key: str = Header(...)):
    # fetch all keys for this API key
    keys_pattern = f"usage:{x_api_key}:*"
    keys = await asyncio.to_thread(redis_client.keys, keys_pattern)
    usage_data = {}
    for key in keys:
        count = await asyncio.to_thread(redis_client.get, key)
        endpoint = key.decode().split(":", 2)[2]  # extract endpoint
        usage_data[endpoint] = int(count)
    return {"api_key": x_api_key, "usage": usage_data}