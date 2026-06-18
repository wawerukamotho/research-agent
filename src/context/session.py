from uuid import UUID
from typing import Any, Dict, List
from context.models import ResearchSession, ResearchPlan, Task, Checkpoint, TaskStatus
from context.budget import TokenBudgetManager
from context.summary import RollingSummaryManager
from context.checkpoint import CheckpointManager

class ResearchSessionManager:
    def __init__(self, query: str, budget_limit: float = 5.0, redis_client: Any = None):
        self.session = ResearchSession(
            query=query,
            plan=ResearchPlan(objectives=[f"Research: {query}"])
        )
        self.budget = TokenBudgetManager(limit=budget_limit)
        self.summary = RollingSummaryManager()
        self.checkpoint = CheckpointManager(redis_client=redis_client)

    async def add_task(self, description: str) -> Task:
        task = Task(description=description)
        self.session.plan.tasks.append(task)
        await self.save()
        return task

    async def complete_task(self, task_id: UUID, result: Any):
        for task in self.session.plan.tasks:
            if task.id == task_id:
                task.status = TaskStatus.COMPLETED
                task.result = result
                self.session.plan.completed_tasks.append(task_id)
                break
        await self.save()

    async def record_tool_execution(self, tool_id: str, task_id: UUID, snapshot: Dict[str, Any]):
        checkpoint = Checkpoint(
            task_id=task_id,
            tool_id=tool_id,
            state_snapshot=snapshot
        )
        self.session.plan.checkpoints.append(checkpoint)
        await self.checkpoint.save_checkpoint(self.session.id, checkpoint)
        await self.save()

    async def update_from_llm_response(self, response: Any):
        # Update budget
        self.budget.update_usage(
            prompt_tokens=response.usage.prompt_tokens,
            completion_tokens=response.usage.completion_tokens,
            cost=getattr(response, "cost", 0.0)
        )
        self.session.token_usage = self.budget.get_usage()

        # Update summary if applicable (simplified)
        await self.summary.update_summary(response.choices[0].message.content)
        self.session.rolling_summary = self.summary.get_summary()
        await self.save()

    async def save(self):
        await self.checkpoint.save_session(self.session)

    @classmethod
    async def resume(cls, session_id: UUID) -> 'ResearchSessionManager':
        # Implementation to restore from Redis
        cm = CheckpointManager()
        session = await cm.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")

        instance = cls(session.query)
        instance.session = session
        instance.budget.usage = session.token_usage
        instance.summary.summary = session.rolling_summary
        return instance
