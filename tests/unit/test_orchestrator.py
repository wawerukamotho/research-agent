import pytest
from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch, AsyncMock

client = TestClient(app)

@pytest.mark.asyncio
async def test_orchestrator_flow():
    # Tools must be registered
    from registry.discovery import discover_tools
    discover_tools()

    with patch("redis.asyncio.Redis.set", new_callable=AsyncMock), \
         patch("redis.asyncio.Redis.rpush", new_callable=AsyncMock), \
         patch("redis.asyncio.Redis.get", new_callable=AsyncMock):

        # Start research
        response = client.post("/research/", json={"query": "Latest AI agents", "max_steps": 2})
        assert response.status_code == 200
        data = response.json()
        session_id = data["session_id"]
        assert data["query"] == "Latest AI agents"

        # Check status
        response = client.get(f"/research/{session_id}")
        assert response.status_code == 200
        assert response.json()["session_id"] == session_id
