import asyncio
import inspect
from typing import Any, List, Dict, Optional
import litellm
import structlog

logger = structlog.get_logger()

async def safe_acompletion(*args, **kwargs) -> Any:
    """
    A defensive wrapper around litellm.acompletion to handle internal coroutine leaks.
    Ensures the response is fully awaited and not a coroutine object.
    """
    try:
        response = await litellm.acompletion(*args, **kwargs)

        # Defensive check: if for some reason we got a coroutine back (internal leak)
        # loop until we get a real response
        while inspect.iscoroutine(response) or asyncio.iscoroutine(response):
            logger.warning("llm_coroutine_leak_detected", type=type(response))
            response = await response

        return response
    except Exception as e:
        logger.error("llm_call_failed", error=str(e), model=kwargs.get("model"))
        raise
