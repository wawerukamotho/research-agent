from typing import Dict, List, Optional, Any, Type
import structlog
from pydantic import BaseModel, ValidationError
from registry.base import BaseTool, ToolMetadata
from scaffold.errors import ToolError, ValidationError as AppValidationError

logger = structlog.get_logger()

class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}

    def register(self, tool: BaseTool):
        tool_id = f"{tool.metadata.namespace}.{tool.metadata.name}"
        if tool_id in self._tools:
            logger.warning("tool_already_registered", tool_id=tool_id)
        self._tools[tool_id] = tool
        logger.info("tool_registered", tool_id=tool_id)

    def get_tool(self, tool_id: str) -> Optional[BaseTool]:
        return self._tools.get(tool_id)

    def list_tools(self, namespace: Optional[str] = None) -> List[ToolMetadata]:
        return [
            tool.metadata
            for tool_id, tool in self._tools.items()
            if namespace is None or tool.metadata.namespace == namespace
        ]

    def get_tool_schemas(self, namespace: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Return tools in OpenAI-compatible function calling format.
        """
        tools = self.list_tools(namespace)
        schemas = []
        for tool in tools:
            schemas.append({
                "type": "function",
                "function": {
                    "name": f"{tool.namespace}_{tool.name}",
                    "description": tool.description,
                    "parameters": tool.input_schema.model_json_schema()
                }
            })
        return schemas

    async def execute(self, tool_id: str, input_params: Dict[str, Any]) -> Any:
        from scaffold.metrics import TOOL_EXECUTION_COUNT, TOOL_LATENCY
        import time
        from opentelemetry import trace

        tracer = trace.get_tracer(__name__)

        tool = self.get_tool(tool_id)
        if not tool:
            TOOL_EXECUTION_COUNT.labels(tool_id=tool_id, status="not_found").inc()
            raise ToolError(f"Tool {tool_id} not found")

        # Validate input
        try:
            validated_input = tool.metadata.input_schema(**input_params)
        except ValidationError as e:
            raise AppValidationError(f"Invalid input for tool {tool_id}", details=e.errors())

        # Execute
        start_time = time.perf_counter()
        try:
            with tracer.start_as_current_span(f"tool_exec:{tool_id}") as span:
                span.set_attribute("tool.id", tool_id)
                logger.info("executing_tool", tool_id=tool_id)
                result = await tool.run(validated_input)

            # Validate output
            if not isinstance(result, tool.metadata.output_schema):
                # If it's a dict, try to convert to schema
                if isinstance(result, dict):
                    result = tool.metadata.output_schema(**result)
                else:
                    raise ToolError(f"Tool {tool_id} returned invalid output type")

            latency = time.perf_counter() - start_time
            TOOL_LATENCY.labels(tool_id=tool_id).observe(latency)
            TOOL_EXECUTION_COUNT.labels(tool_id=tool_id, status="success").inc()

            return result
        except Exception as e:
            TOOL_EXECUTION_COUNT.labels(tool_id=tool_id, status="error").inc()
            logger.error("tool_execution_failed", tool_id=tool_id, error=str(e))
            if isinstance(e, ToolError):
                raise e
            raise ToolError(f"Execution of {tool_id} failed: {str(e)}")

# Global registry instance
registry = ToolRegistry()
