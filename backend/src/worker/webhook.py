import logging

import httpx

logger = logging.getLogger(__name__)


async def send_webhook(
    webhook_url: str,
    payload: dict,
    timeout: float = 5
) -> bool:
    async with httpx.AsyncClient(timeout=timeout) as client:
        logger.info(f"Sending a webhook to {webhook_url}")
        response = await client.post(webhook_url, json=payload)
        response.raise_for_status()
        logger.info(f"Webhook sussessfully sent, status: {response.status_code}")
        return True
