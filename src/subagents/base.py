from typing import List, Dict, Any, Optional, Type
from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from registry.registry import registry
from registry.base import BaseTool

class SubagentContext(BaseModel):
    session_id: UUID = Field(default_factory=uuid4)
    memory: List[Dict[str, Any]] = Field(default_factory=list)
    variables: Dict[str, Any] = Field(default_factory=dict)

class SubagentToolRegistry:
    def __init__(self, allowed_tools: List[str]):
        self._allowed_tools = allowed_tools

    async def execute(self, tool_id: str, params: Dict[str, Any], subagent_name: str = "unknown") -> Any:
        from scaffold.metrics import SUBAGENT_TOOL_CALLS
        if tool_id not in self._allowed_tools:
            raise PermissionError(f"Tool {tool_id} is not in the subagent's scope.")

        SUBAGENT_TOOL_CALLS.labels(subagent_name=subagent_name, tool_id=tool_id).inc()
        return await registry.execute(tool_id, params)

    def list_tools(self) -> List[Any]:
        return [registry.get_tool(tid).metadata for tid in self._allowed_tools if registry.get_tool(tid)]

class BaseSubagent:
    def __init__(self, name: str, scope: List[str]):
        self.name = name
        self.context = SubagentContext()
        self.tools = SubagentToolRegistry(scope)

    async def run(self, input_data: Any) -> Any:
        from scaffold.metrics import SUBAGENT_RUN_COUNT, SUBAGENT_RUNTIME
        import time
        from opentelemetry import trace

        tracer = trace.get_tracer(__name__)
        start_time = time.perf_counter()

        try:
            with tracer.start_as_current_span(f"subagent_run:{self.name}") as span:
                span.set_attribute("subagent.name", self.name)
                result = await self._run_logic(input_data)

            latency = time.perf_counter() - start_time
            SUBAGENT_RUNTIME.labels(subagent_name=self.name).observe(latency)
            SUBAGENT_RUN_COUNT.labels(subagent_name=self.name, status="success").inc()
            return result
        except Exception as e:
            SUBAGENT_RUN_COUNT.labels(subagent_name=self.name, status="error").inc()
            raise

    async def _run_logic(self, input_data: Any) -> Any:
        raise NotImplementedError
