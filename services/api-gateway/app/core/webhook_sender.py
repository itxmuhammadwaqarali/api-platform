import httpx

async def send_webhook(url: str, payload: dict):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=payload, timeout=5)
            return response.status_code
        except Exception as e:
            print(f"Webhook failed for {url}: {e}")
            return None