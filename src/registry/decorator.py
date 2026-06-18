from typing import Any, Callable, Type
from pydantic import BaseModel
from registry.base import BaseTool, ToolMetadata
from registry.registry import registry

def tool(
    name: str,
    namespace: str,
    description: str,
    input_schema: Type[BaseModel],
    output_schema: Type[BaseModel],
):
    """
    Decorator for registering tools.
    """
    def decorator(cls: Type[BaseTool]):
        # Ensure it's a subclass of BaseTool
        if not issubclass(cls, BaseTool):
            raise TypeError(f"Class {cls.__name__} must inherit from BaseTool")

        # Instantiate and set metadata
        tool_instance = cls()
        tool_instance.metadata = ToolMetadata(
            name=name,
            namespace=namespace,
            description=description,
            input_schema=input_schema,
            output_schema=output_schema
        )

        # Register with the global registry
        registry.register(tool_instance)
        return cls

    return decorator
