from uuid import UUID
from typing import Any, Dict, List, Optional
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from context.models import ResearchSession, Task, Checkpoint, TaskStatus
from context.budget import TokenBudgetManager
from context.summary import RollingSummaryManager
from context.checkpoint import CheckpointManager

class ResearchSessionManager:
    def __init__(self, query: str, budget_limit: float = 5.0, redis_client: Any = None, db_engine: Any = None):
        self.session = ResearchSession(
            query=query
        )
        self.budget = TokenBudgetManager(limit=budget_limit)
        self.summary = RollingSummaryManager()
        self.checkpoint = CheckpointManager(redis_client=redis_client)
        self.db_engine = db_engine

    async def add_task(self, description: str) -> Task:
        task = Task(session_id=self.session.id, description=description)
        async with AsyncSession(self.db_engine) as db_session:
            db_session.add(task)
            await db_session.commit()
            await db_session.refresh(task)
        return task

    async def get_tasks(self) -> List[Task]:
        async with AsyncSession(self.db_engine) as db_session:
            statement = select(Task).where(Task.session_id == self.session.id)
            results = await db_session.execute(statement)
            return list(results.scalars().all())

    async def complete_task(self, task_id: UUID, result: Any):
        async with AsyncSession(self.db_engine) as db_session:
            task = await db_session.get(Task, task_id)
            if task:
                task.status = TaskStatus.COMPLETED
                task.result = result if isinstance(result, dict) else {"data": str(result)}
                from datetime import datetime, UTC
                task.completed_at = datetime.now(UTC)
                db_session.add(task)
                await db_session.commit()
        await self.save()

    async def record_tool_execution(self, tool_id: str, task_id: UUID, snapshot: Dict[str, Any]):
        checkpoint = Checkpoint(
            session_id=self.session.id,
            task_id=task_id,
            tool_id=tool_id,
            state_snapshot=snapshot
        )
        async with AsyncSession(self.db_engine) as db_session:
            db_session.add(checkpoint)
            await db_session.commit()

        await self.checkpoint.save_checkpoint(self.session.id, checkpoint)
        await self.save()

    async def update_from_llm_response(self, response: Any):
        self.budget.update_usage(
            prompt_tokens=response.usage.prompt_tokens,
            completion_tokens=response.usage.completion_tokens,
            cost=getattr(response, "cost", 0.0)
        )
        usage = self.budget.get_usage()
        self.session.prompt_tokens = usage.prompt_tokens
        self.session.completion_tokens = usage.completion_tokens
        self.session.total_tokens = usage.total_tokens
        self.session.total_cost = usage.cost

        await self.summary.update_summary(response.choices[0].message.content)
        self.session.rolling_summary = self.summary.get_summary()
        await self.save()

    async def save(self):
        async with AsyncSession(self.db_engine) as db_session:
            db_session.add(self.session)
            await db_session.commit()
            await db_session.refresh(self.session)
        await self.checkpoint.save_session(self.session)

    @classmethod
    async def resume(cls, session_id: UUID, db_engine: Any) -> 'ResearchSessionManager':
        async with AsyncSession(db_engine) as db_session:
            session = await db_session.get(ResearchSession, session_id)
            if not session:
                raise ValueError(f"Session {session_id} not found")

            instance = cls(session.query, db_engine=db_engine)
            instance.session = session
            instance.budget.usage.prompt_tokens = session.prompt_tokens
            instance.budget.usage.completion_tokens = session.completion_tokens
            instance.budget.usage.total_tokens = session.total_tokens
            instance.budget.usage.cost = session.total_cost
            instance.summary.summary = session.rolling_summary
            return instance
