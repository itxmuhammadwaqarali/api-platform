from asgiref.sync import sync_to_async
from usage.utils import log_api_usage

async def log_usage(api_key, endpoint, method):
    await sync_to_async(log_api_usage)(api_key, endpoint, method)
