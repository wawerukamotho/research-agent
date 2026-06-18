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

    async def execute(self, tool_id: str, params: Dict[str, Any]) -> Any:
        if tool_id not in self._allowed_tools:
            raise PermissionError(f"Tool {tool_id} is not in the subagent's scope.")
        return await registry.execute(tool_id, params)

    def list_tools(self) -> List[Any]:
        return [registry.get_tool(tid).metadata for tid in self._allowed_tools if registry.get_tool(tid)]

class BaseSubagent:
    def __init__(self, name: str, scope: List[str]):
        self.name = name
        self.context = SubagentContext()
        self.tools = SubagentToolRegistry(scope)

    async def run(self, input_data: Any) -> Any:
        raise NotImplementedError
