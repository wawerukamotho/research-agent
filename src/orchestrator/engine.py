import json
import asyncio
from typing import List, Dict, Any, Optional
from uuid import UUID
import structlog
from scaffold.llm import safe_acompletion
from orchestrator.models import ResearchRequest, ResearchStatus, OrchestratorEvent
from context.session import ResearchSessionManager
from registry.registry import registry
from scaffold.config import settings
from scaffold.errors import SubagentError, ToolError

logger = structlog.get_logger()

class Orchestrator:
    def __init__(self, request: ResearchRequest, redis_client: Any = None, db_engine: Any = None):
        self.request = request
        self.session_manager = ResearchSessionManager(
            query=request.query,
            budget_limit=request.budget_limit,
            redis_client=redis_client,
            db_engine=db_engine
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
                next_task = await self._get_next_pending_task()
                if not next_task:
                    logger.info("all_tasks_completed")
                    break

                await self._execute_task(next_task)
                self.step_count += 1

                # Check for plan updates/refinement
                await self._refine_plan()

            self.session_manager.session.status = "finished"
            await self.session_manager.save()
            logger.info("orchestrator_finished", session_id=str(self.session_manager.session.id))

        except Exception as e:
            logger.exception("orchestrator_failed", error=str(e))
            self.is_running = False
            raise

    async def _generate_initial_plan(self):
        prompt = f"Create a multi-step research plan for: {self.request.query}. Return a list of tasks."

        try:
            response = await safe_acompletion(
                model=settings.default_llm_model,
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            # Update session with LLM results (budget/summary)
            await self.session_manager.update_from_llm_response(response)

            # For demonstration, we'll still add baseline tasks if LLM doesn't return list
            await self.session_manager.add_task("Decompose the research question into core themes.")
            await self.session_manager.add_task("Identify 5 key sources using web search.")
            await self.session_manager.add_task("Extract claims from identified sources.")

        except Exception as e:
            logger.error("plan_generation_failed", error=str(e))
            await self.session_manager.add_task("Decompose the research question into core themes.")
            await self.session_manager.add_task("Identify 5 key sources using web search.")

        logger.info("initial_plan_generated")

    async def _get_next_pending_task(self) -> Optional[Any]:
        tasks = await self.session_manager.get_tasks()
        for task in tasks:
            from context.models import TaskStatus
            if task.status == TaskStatus.PENDING:
                return task
        return None

    async def _execute_task(self, task: Any):
        logger.info("executing_task", task_id=str(task.id), description=task.description)
        from context.models import TaskStatus
        task.status = TaskStatus.IN_PROGRESS

        # Decide which tool or subagent to use
        tool_id = await self._select_tool_for_task(task)

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

    async def _select_tool_for_task(self, task: Any) -> str:
        """
        Model-driven tool selection using the registry's JSON schemas.
        """
        schemas = registry.get_tool_schemas()
        prompt = f"""
        Given the task: "{task.description}"
        And the following available tools:
        {json.dumps(schemas, indent=2)}

        Select the best tool to complete this task. Return ONLY the tool ID in the format 'namespace.name'.
        """

        try:
            response = await safe_acompletion(
                model=settings.default_llm_model,
                messages=[{"role": "user", "content": prompt}]
            )
            tool_choice = response.choices[0].message.content.strip()
            # Standardize format if LLM uses underscores (OpenAI style)
            tool_choice = tool_choice.replace("_", ".", 1)

            if registry.get_tool(tool_choice):
                return tool_choice
        except Exception as e:
            logger.error("model_tool_selection_failed", error=str(e))

        # Fallback logic
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
        tasks = await self.session_manager.get_tasks()
        completed_count = sum(1 for t in tasks if t.status == "completed")
        next_task = await self._get_next_pending_task()

        return ResearchStatus(
            session_id=session.id,
            query=session.query,
            status=session.status,
            progress=completed_count / max(len(tasks), 1),
            current_task=next_task.description if next_task else None,
            step_count=self.step_count,
            created_at=session.created_at,
            updated_at=session.updated_at
        )
