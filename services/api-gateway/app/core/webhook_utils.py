import httpx
import asyncio

async def trigger_webhook(url: str, payload: dict):
    """
    Send POST request to webhook URL asynchronously
    """
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.post(url, json=payload)
            return response.status_code, response.text
    except Exception as e:
        print(f"Webhook error for {url}: {e}")
        return None, str(e)