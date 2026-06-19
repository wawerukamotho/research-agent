import pytest
from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch, AsyncMock

@pytest.mark.asyncio
async def test_orchestrator_flow():
    # Tools must be registered
    from registry.discovery import discover_tools
    discover_tools()

    mock_session_manager = AsyncMock()
    mock_session_manager.session.id = "00000000-0000-0000-0000-000000000000"
    mock_session_manager.session.query = "Latest AI agents"
    mock_session_manager.session.status = "PENDING"
    mock_session_manager.get_tasks.return_value = []

    with patch("redis.asyncio.Redis.set", new_callable=AsyncMock), \
         patch("redis.asyncio.Redis.rpush", new_callable=AsyncMock), \
         patch("redis.asyncio.Redis.get", new_callable=AsyncMock), \
         patch("context.session.ResearchSessionManager.save", new_callable=AsyncMock), \
         patch("context.session.ResearchSessionManager.resume", return_value=mock_session_manager), \
         patch("orchestrator.engine.Orchestrator.run", new_callable=AsyncMock), \
         TestClient(app) as client:

        # Start research
        response = client.post("/research/", json={"query": "Latest AI agents", "max_steps": 2})
        assert response.status_code == 200
        data = response.json()
        session_id = data["session_id"]

        # Check status
        response = client.get(f"/research/{session_id}")
        assert response.status_code == 200
        assert response.json()["query"] == "Latest AI agents"
