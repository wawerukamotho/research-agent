import pytest
from fastapi.testclient import TestClient
from main import app
from registry.registry import registry
from unittest.mock import patch, AsyncMock, MagicMock

client = TestClient(app)

def test_tool_discovery_on_startup():
    # Use the TestClient in a context manager to trigger lifespan events
    with TestClient(app) as client:
        # Check if tools from all namespaces are registered
        search_tools = registry.list_tools(namespace="search")
        fetch_tools = registry.list_tools(namespace="fetch")
        analyze_tools = registry.list_tools(namespace="analyze")
        write_tools = registry.list_tools(namespace="write")

        assert len(search_tools) >= 14
        assert len(fetch_tools) >= 13
        assert len(analyze_tools) >= 13
        assert len(write_tools) >= 12

        # Verify a specific tool existence
        web_search = registry.get_tool("search.web_search")
        assert web_search is not None
        assert web_search.metadata.name == "web_search"

def test_http_client_in_state():
    with TestClient(app) as client:
        assert hasattr(app.state, "http_client")
        import httpx
        assert isinstance(app.state.http_client, httpx.AsyncClient)
