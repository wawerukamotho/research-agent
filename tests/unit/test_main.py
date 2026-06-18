import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "version": "0.1.0"}

from unittest.mock import patch, AsyncMock

def test_ready_check():
    with patch("main.create_async_engine") as mock_engine, \
         patch("redis.asyncio.from_url") as mock_redis:

        # Mock Postgres
        mock_engine_instance = AsyncMock()
        mock_engine.return_value = mock_engine_instance

        mock_conn = AsyncMock()
        mock_engine_instance.connect.return_value = mock_conn

        # Mock Redis
        mock_redis_client = AsyncMock()
        mock_redis.return_value = mock_redis_client

        response = client.get("/ready")
        assert response.status_code == 200
        assert response.json() == {"status": "ready"}

def test_app_error_handler():
    from scaffold.errors import AppError

    @app.get("/test-error")
    async def trigger_error():
        raise AppError("Test error", code="TEST_CODE", details={"foo": "bar"})

    response = client.get("/test-error")
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "TEST_CODE"
    assert response.json()["error"]["details"] == {"foo": "bar"}
