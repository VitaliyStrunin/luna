import asyncio
import logging
from typing import Any, Callable

logger = logging.getLogger(__name__)


async def retry_with_backoff(
    func: Callable[..., Any],
    max_attempts: int = 3,
    base_delay: float = 1.0,
    exponential_base: float = 2.0,
    *args,
    **kwargs
) -> Any:

    last_exception = None

    for attempt in range(max_attempts):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            last_exception = e
            if attempt < max_attempts - 1:
                delay = base_delay * (exponential_base ** attempt)
                logger.warning(
                    f"Attempt {attempt + 1}/{max_attempts} failed "
                    f"Next attempt in {delay}s. Error: {e}"
                )
                await asyncio.sleep(delay)
            else:
                logger.error(
                    f" All attempts failed, last error: {e}"
                )

    raise last_exception
