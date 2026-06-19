import asyncio
import time
from typing import Callable, Any, Dict, Optional
import structlog
from scaffold.errors import RateLimitError, ToolError

logger = structlog.get_logger()

class TokenBucket:
    def __init__(self, capacity: int, fill_rate: float):
        self.capacity = capacity
        self.fill_rate = fill_rate
        self.tokens = capacity
        self.last_fill = time.monotonic()

    async def consume(self, tokens: int = 1):
        now = time.monotonic()
        elapsed = now - self.last_fill
        self.tokens = min(self.capacity, self.tokens + elapsed * self.fill_rate)
        self.last_fill = now

        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False

class RateLimiter:
    def __init__(self, capacity: int = 10, fill_rate: float = 1.0):
        self.bucket = TokenBucket(capacity, fill_rate)

    async def wait(self):
        while not await self.bucket.consume():
            await asyncio.sleep(0.1)

class RetryManager:
    def __init__(self, max_retries: int = 5, base_delay: float = 1.0, jitter: float = 0.1):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.jitter = jitter

    async def execute(self, func: Callable, *args, **kwargs) -> Any:
        import random
        retries = 0
        while retries <= self.max_retries:
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                if retries == self.max_retries:
                    raise e

                delay = self.base_delay * (2 ** retries) + (random.random() * self.jitter)
                logger.warning("retrying_execution", retry=retries + 1, delay=delay, error=str(e))
                await asyncio.sleep(delay)
                retries += 1

class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, recovery_timeout: float = 30.0):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failures = 0
        self.state = "closed" # closed, open, half-open
        self.last_failure_time = 0

    async def call(self, func: Callable, *args, **kwargs) -> Any:
        if self.state == "open":
            if time.monotonic() - self.last_failure_time > self.recovery_timeout:
                self.state = "half-open"
            else:
                raise ToolError("Circuit breaker is open")

        try:
            result = await func(*args, **kwargs)
            self.failures = 0
            self.state = "closed"
            return result
        except Exception as e:
            self.failures += 1
            self.last_failure_time = time.monotonic()
            if self.failures >= self.failure_threshold:
                self.state = "open"
                logger.error("circuit_breaker_opened")
            raise e
