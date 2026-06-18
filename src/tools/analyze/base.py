from abc import ABC, abstractmethod
from typing import Any, Dict, List
from tools.analyze.models import AnalysisInput

class AnalysisProvider(ABC):
    @abstractmethod
    async def analyze(self, text: str, task: str, schema: Any, context: str = None) -> Any:
        pass
