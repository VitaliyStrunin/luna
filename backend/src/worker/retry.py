import asyncio
from typing import Callable, Any


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
                print(f"Attempt {attempt + 1}/{max_attempts} failed. Retry in {delay}s...")
                await asyncio.sleep(delay)
    
    raise last_exception