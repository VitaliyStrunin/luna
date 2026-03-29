import httpx


async def send_webhook(
    webhook_url: str,
    payload: dict,
    timeout: float = 5
) -> bool:
    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.post(webhook_url, json=payload)
        response.raise_for_status()
        return True