import pytest
from unittest.mock import patch, AsyncMock
from registry.registry import registry
from tools.write.models import WriteResponse, OutlineResponse, ReportResponse

@pytest.mark.asyncio
async def test_all_write_tools_registered():
    import tools.write.tools
    write_tools = registry.list_tools(namespace="write")
    expected_tools = {
        "draft_section", "write_introduction", "write_conclusion",
        "format_citation", "assemble_report", "add_inline_citation",
        "generate_executive_summary", "export_markdown", "export_json",
        "create_outline", "suggest_followup_questions", "validate_report_structure"
    }
    registered_names = {t.name for t in write_tools}
    assert expected_tools.issubset(registered_names)

@pytest.mark.asyncio
async def test_draft_section_execution():
    import tools.write.tools
    with patch("tools.write.provider.litellm.acompletion") as mock_completion:
        mock_completion.return_value = AsyncMock(
            choices=[
                AsyncMock(
                    message=AsyncMock(
                        content='{"content": "Drafted content for AI agents...", "metadata": {}}'
                    )
                )
            ]
        )

        result = await registry.execute("write.draft_section", {"prompt": "Draft section about AI agents."})
        assert isinstance(result, WriteResponse)
        assert "AI agents" in result.content

@pytest.mark.asyncio
async def test_assemble_report_execution():
    import tools.write.tools
    data = {
        "title": "AI Report",
        "executive_summary": {
            "summary": "AI is evolving.",
            "key_findings": ["Fast growth"],
            "confidence_score": 0.95
        },
        "sections": [
            {
                "title": "Intro",
                "content": "Welcome to AI.",
                "citations": []
            }
        ],
        "bibliography": []
    }

    result = await registry.execute("write.assemble_report", data)
    assert isinstance(result, ReportResponse)
    assert result.report.title == "AI Report"
    assert len(result.report.sections) == 1
