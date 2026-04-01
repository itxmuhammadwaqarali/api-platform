from fastapi import FastAPI
from app.api.v1.router import router as v1_router
from app.middleware.api_key_middleware import APIKeyMiddleware

app = FastAPI(title="API Platform Gateway")

app.add_middleware(APIKeyMiddleware)

app.include_router(v1_router, prefix="/v1")