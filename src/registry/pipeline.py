import asyncio
import structlog
from typing import List, Any, Dict, Callable, Optional
from pydantic import BaseModel, ConfigDict
from registry.registry import registry
from scaffold.errors import ToolError

logger = structlog.get_logger()

class PipelineStep(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    tool_id: str
    input_mapper: Optional[Callable[[Any], Dict[str, Any]]] = None

class ToolPipeline:
    def __init__(self, name: str):
        self.name = name
        self.steps: List[PipelineStep] = []

    def add_step(self, tool_id: str, input_mapper: Callable[[Any], Dict[str, Any]] = None):
        self.steps.append(PipelineStep(tool_id=tool_id, input_mapper=input_mapper))
        return self

    async def execute(self, initial_input: Dict[str, Any]) -> Any:
        logger.info("pipeline_started", pipeline=self.name)
        current_data = initial_input

        for step in self.steps:
            logger.info("pipeline_step_executing", tool_id=step.tool_id)

            # Map data from previous step if mapper exists
            if step.input_mapper:
                current_data = step.input_mapper(current_data)

            # Execute tool
            current_data = await registry.execute(step.tool_id, current_data)

            # If output is Pydantic model, convert to dict for next step mapping if needed
            # but usually we want to keep it structured.

        logger.info("pipeline_completed", pipeline=self.name)
        return current_data
