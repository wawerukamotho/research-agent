import pytest
import asyncio
from scaffold.resilience import RetryManager, RateLimiter, TokenBucket

@pytest.mark.asyncio
async def test_retry_manager_success():
    retry = RetryManager(max_retries=2)
    counter = 0

    async def failing_func():
        nonlocal counter
        if counter < 2:
            counter += 1
            raise ValueError("Fail")
        return "Success"

    result = await retry.execute(failing_func)
    assert result == "Success"
    assert counter == 2

@pytest.mark.asyncio
async def test_rate_limiter():
    # Capacity 1, fill rate 10 per second
    limiter = RateLimiter(capacity=1, fill_rate=10.0)

    start = asyncio.get_event_loop().time()
    await limiter.wait()
    await limiter.wait()
    end = asyncio.get_event_loop().time()

    # Second wait should have taken around 0.1s
    assert end - start >= 0.05
