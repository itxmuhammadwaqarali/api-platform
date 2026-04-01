import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from app.api.v1.router import router as v1_router
from app.middleware.api_key_middleware import APIKeyMiddleware
from app.middleware.rate_limit_middleware import RateLimitMiddleware


app = FastAPI(title="API Platform Gateway")

app.add_middleware(APIKeyMiddleware)
app.add_middleware(RateLimitMiddleware, limit=5, window=60)

app.include_router(v1_router, prefix="/v1")

@app.get("/test-key")
def test_key():
    return {"message": "API Key validated"}

