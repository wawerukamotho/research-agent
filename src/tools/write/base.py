from abc import ABC, abstractmethod
from typing import Any

class WriteProvider(ABC):
    @abstractmethod
    async def generate(self, prompt: str, task: str, schema: Any, context: str = None) -> Any:
        pass
