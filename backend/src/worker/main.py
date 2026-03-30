import asyncio
import logging

from src.worker.consumer import app


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def run_worker():
    logger.info("Starting worker service")

    try:
        await app.run()  
    except Exception as e:
        logger.error(f"Worker error: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    asyncio.run(run_worker())