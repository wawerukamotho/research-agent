import json
import asyncio
from typing import List, Dict, Any, Optional
from uuid import UUID
import litellm
import structlog
from orchestrator.models import ResearchRequest, ResearchStatus, OrchestratorEvent
from context.session import ResearchSessionManager
from registry.registry import registry
from scaffold.config import settings
from scaffold.errors import SubagentError, ToolError

logger = structlog.get_logger()

class Orchestrator:
    def __init__(self, request: ResearchRequest):
        self.request = request
        self.session_manager = ResearchSessionManager(
            query=request.query,
            budget_limit=request.budget_limit
        )
        self.step_count = 0
        self.is_running = False

    async def run(self):
        from opentelemetry import trace
        tracer = trace.get_tracer(__name__)

        self.is_running = True
        logger.info("orchestrator_started", query=self.request.query)

        try:
            with tracer.start_as_current_span("research_orchestration") as span:
                span.set_attribute("research.query", self.request.query)
                span.set_attribute("session.id", str(self.session_manager.session.id))
            # 1. Initial Plan Generation
            await self._generate_initial_plan()

            # 2. Main Execution Loop
            while self.is_running and self.step_count < self.request.max_steps:
                next_task = self._get_next_pending_task()
                if not next_task:
                    logger.info("all_tasks_completed")
                    break

                await self._execute_task(next_task)
                self.step_count += 1

                # Check for plan updates/refinement
                await self._refine_plan()

            logger.info("orchestrator_finished", session_id=str(self.session_manager.session.id))

        except Exception as e:
            logger.exception("orchestrator_failed", error=str(e))
            self.is_running = False
            raise

    async def _generate_initial_plan(self):
        prompt = f"Create a multi-step research plan for: {self.request.query}"
        # In a real system, this would call LLM to generate tasks.
        # For Phase 9 implementation, we provide a structured starting point.
        await self.session_manager.add_task("Decompose the research question into core themes.")
        await self.session_manager.add_task("Identify 5 key sources using web search.")
        await self.session_manager.add_task("Extract claims from identified sources.")
        logger.info("initial_plan_generated")

    def _get_next_pending_task(self) -> Optional[Any]:
        for task in self.session_manager.session.plan.tasks:
            from context.models import TaskStatus
            if task.status == TaskStatus.PENDING:
                return task
        return None

    async def _execute_task(self, task: Any):
        logger.info("executing_task", task_id=str(task.id), description=task.description)
        from context.models import TaskStatus
        task.status = TaskStatus.IN_PROGRESS

        # Decide which tool or subagent to use
        # For Phase 9, we simulate tool selection
        tool_id = self._select_tool_for_task(task)

        try:
            # Execute tool
            result = await registry.execute(tool_id, {"query": task.description} if "search" in tool_id else {"text": "..."})

            # Record execution and checkpoint
            await self.session_manager.record_tool_execution(
                tool_id=tool_id,
                task_id=task.id,
                snapshot={"result": str(result)}
            )

            # Update task status
            await self.session_manager.complete_task(task.id, result=result)

        except Exception as e:
            logger.error("task_execution_failed", task_id=str(task.id), error=str(e))
            from context.models import TaskStatus
            task.status = TaskStatus.FAILED
            raise

    def _select_tool_for_task(self, task: Any) -> str:
        # Mock tool selection logic
        if "search" in task.description.lower():
            return "search.web_search"
        if "extract" in task.description.lower():
            return "analyze.extract_claims"
        return "analyze.summarize_text"

    async def _refine_plan(self):
        # Logic to update plan based on new findings
        pass

    async def get_status(self) -> ResearchStatus:
        session = self.session_manager.session
        from datetime import datetime, UTC
        return ResearchStatus(
            session_id=session.id,
            query=session.query,
            status="running" if self.is_running else "finished",
            progress=len(session.plan.completed_tasks) / max(len(session.plan.tasks), 1),
            current_task=self._get_next_pending_task().description if self._get_next_pending_task() else None,
            step_count=self.step_count,
            created_at=session.plan.tasks[0].created_at if session.plan.tasks else session.metadata.get("created_at", datetime.now(UTC)),
            updated_at=datetime.now(UTC)
        )
