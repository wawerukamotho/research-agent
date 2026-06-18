from context.models import TokenUsage
from scaffold.errors import ContextBudgetError
from scaffold.logging import logger

class TokenBudgetManager:
    def __init__(self, limit: float = 5.0): # Default $5 budget
        self.limit = limit
        self.usage = TokenUsage()

    def update_usage(self, prompt_tokens: int, completion_tokens: int, cost: float):
        self.usage.prompt_tokens += prompt_tokens
        self.usage.completion_tokens += completion_tokens
        self.usage.total_tokens += (prompt_tokens + completion_tokens)
        self.usage.cost += cost

        logger.info("token_usage_updated", total_cost=self.usage.cost, limit=self.limit)

        if self.usage.cost > self.limit:
            raise ContextBudgetError(f"Token budget exceeded: ${self.usage.cost:.4f} > ${self.limit:.4f}")

    def get_usage(self) -> TokenUsage:
        return self.usage
