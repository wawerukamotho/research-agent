import pytest
from prometheus_client import REGISTRY
from registry.registry import registry

@pytest.mark.asyncio
async def test_tool_metrics_collection():
    # Tools must be registered
    from registry.discovery import discover_tools
    discover_tools()

    # Execute a tool
    await registry.execute("search.web_search", {"query": "test"})

    # Check if metrics are recorded
    metric = REGISTRY.get_sample_value("tool_execution_total", {"tool_id": "search.web_search", "status": "success"})
    assert metric is not None
    assert metric >= 1.0

@pytest.mark.asyncio
async def test_subagent_metrics_collection():
    from subagents.fact_checker import FactCheckerSubagent, FactCheckerInput
    from tools.analyze.models import Claim

    subagent = FactCheckerSubagent()
    await subagent.run(FactCheckerInput(claims=[Claim(claim="test", confidence=0.5)]))

    metric = REGISTRY.get_sample_value("subagent_run_total", {"subagent_name": "FactChecker", "status": "success"})
    assert metric is not None
    assert metric >= 1.0
