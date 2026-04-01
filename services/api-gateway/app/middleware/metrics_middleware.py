# app/middleware/metrics_middleware.py
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

# Counters per API key and endpoint
REQUEST_COUNT = Counter(
    "api_requests_total",
    "Total API requests",
    ["api_key", "endpoint", "method"]
)

class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        api_key = request.headers.get("X-API-Key", "anonymous")
        endpoint = request.url.path
        method = request.method

        # Increment the counter
        REQUEST_COUNT.labels(api_key=api_key, endpoint=endpoint, method=method).inc()

        response = await call_next(request)
        return response