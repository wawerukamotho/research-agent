import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "version": "0.1.0"}

from unittest.mock import patch, AsyncMock, MagicMock

def test_ready_check():
    # Inject mock state manually since lifespan doesn't run in TestClient by default
    app.state.db_engine = MagicMock()
    app.state.redis = AsyncMock()

    # Mock Postgres
    mock_conn = AsyncMock()
    app.state.db_engine.connect.return_value.__aenter__.return_value = mock_conn

    # Mock Redis
    app.state.redis.ping = AsyncMock()

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
