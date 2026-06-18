from abc import ABC, abstractmethod
from typing import Any, Dict, Type
from pydantic import BaseModel, Field


class ToolMetadata(BaseModel):
    name: str
    description: str
    namespace: str
    input_schema: Type[BaseModel]
    output_schema: Type[BaseModel]


class BaseTool(ABC):
    """
    Abstract base class for all tools in the system.
    """
    metadata: ToolMetadata

    @abstractmethod
    async def run(self, input_data: Any) -> Any:
        """
        Execute the tool's logic.
        """
        pass
