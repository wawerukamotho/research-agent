import pytest
from uuid import uuid4
from unittest.mock import patch, AsyncMock
from context.session import ResearchSessionManager
from context.models import TaskStatus
from scaffold.errors import ContextBudgetError

@pytest.mark.asyncio
async def test_session_task_management():
    mock_redis = AsyncMock()
    manager = ResearchSessionManager(query="AI trends", redis_client=mock_redis)
    task = await manager.add_task("Search for recent LLM papers")
    assert task.status == TaskStatus.PENDING

    await manager.complete_task(task.id, result={"papers": ["paper1"]})
    assert task.status == TaskStatus.COMPLETED
    assert manager.session.plan.completed_tasks[0] == task.id

@pytest.mark.asyncio
async def test_token_budget_enforcement():
    mock_redis = AsyncMock()
    manager = ResearchSessionManager(query="AI trends", budget_limit=0.01, redis_client=mock_redis)

    class MockUsage:
        def __init__(self):
            self.prompt_tokens = 100
            self.completion_tokens = 100

    class MockResponse:
        def __init__(self):
            self.usage = MockUsage()
            self.cost = 0.02
            self.choices = [AsyncMock()]
            self.choices[0].message.content = "New summary"

    with pytest.raises(ContextBudgetError):
        await manager.update_from_llm_response(MockResponse())

@pytest.mark.asyncio
async def test_session_checkpointing():
    mock_redis = AsyncMock()
    manager = ResearchSessionManager(query="AI trends", redis_client=mock_redis)
    task = await manager.add_task("Test task")

    await manager.record_tool_execution(
        tool_id="search.web_search",
        task_id=task.id,
        snapshot={"results": []}
    )

    assert mock_redis.rpush.called
    assert mock_redis.set.called
