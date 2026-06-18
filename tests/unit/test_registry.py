import pytest
from pydantic import BaseModel
from registry.base import BaseTool
from registry.registry import ToolRegistry
from registry.decorator import tool
from scaffold.errors import ValidationError, ToolError

class MockInput(BaseModel):
    query: str

class MockOutput(BaseModel):
    result: str

class MockTool(BaseTool):
    async def run(self, input_data: MockInput) -> MockOutput:
        return MockOutput(result=f"Processed: {input_data.query}")

@pytest.fixture
def registry():
    return ToolRegistry()

@pytest.mark.asyncio
async def test_registry_registration_and_execution(registry):
    mock_tool = MockTool()
    from registry.base import ToolMetadata
    mock_tool.metadata = ToolMetadata(
        name="test_tool",
        namespace="test",
        description="A test tool",
        input_schema=MockInput,
        output_schema=MockOutput
    )

    registry.register(mock_tool)

    # Successful execution
    result = await registry.execute("test.test_tool", {"query": "hello"})
    assert result.result == "Processed: hello"

    # Invalid input
    with pytest.raises(ValidationError):
        await registry.execute("test.test_tool", {"wrong_key": "hello"})

    # Tool not found
    with pytest.raises(ToolError):
        await registry.execute("non.existent", {"query": "hello"})

def test_decorator_registration():
    from registry.registry import registry as global_registry

    @tool(
        name="decorated_tool",
        namespace="test",
        description="A decorated test tool",
        input_schema=MockInput,
        output_schema=MockOutput
    )
    class DecoratedTool(BaseTool):
        async def run(self, input_data: MockInput) -> MockOutput:
            return MockOutput(result=input_data.query)

    tool_instance = global_registry.get_tool("test.decorated_tool")
    assert tool_instance is not None
    assert tool_instance.metadata.name == "decorated_tool"
    assert tool_instance.metadata.namespace == "test"

def test_json_schema_generation(registry):
    mock_tool = MockTool()
    from registry.base import ToolMetadata
    mock_tool.metadata = ToolMetadata(
        name="test_tool",
        namespace="test",
        description="A test tool",
        input_schema=MockInput,
        output_schema=MockOutput
    )
    registry.register(mock_tool)

    schemas = registry.get_tool_schemas()
    assert len(schemas) == 1
    assert schemas[0]["function"]["name"] == "test_test_tool"
    assert "query" in schemas[0]["function"]["parameters"]["properties"]
