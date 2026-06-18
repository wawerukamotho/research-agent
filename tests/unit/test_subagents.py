import pytest
from subagents.fact_checker import FactCheckerSubagent, FactCheckerInput
from subagents.section_writer import SectionWriterSubagent, SectionWriterInput
from subagents.citation_validator import CitationValidatorSubagent, CitationValidatorInput
from tools.analyze.models import Claim
from tools.write.models import SectionBrief

@pytest.mark.asyncio
async def test_fact_checker_isolated_tools():
    # Tools must be registered
    from registry.discovery import discover_tools
    discover_tools()

    subagent = FactCheckerSubagent()

    # Should be able to list tools in its scope
    tools = subagent.tools.list_tools()
    assert len(tools) == 7
    assert any(t.name == "web_search" for t in tools)

    # Should NOT be able to execute tool outside its scope
    with pytest.raises(PermissionError):
        await subagent.tools.execute("write.assemble_report", {})

@pytest.mark.asyncio
async def test_fact_checker_run():
    subagent = FactCheckerSubagent()
    input_data = FactCheckerInput(claims=[Claim(claim="The sky is blue", confidence=1.0)])
    output = await subagent.run(input_data)
    assert len(output.results) == 1
    assert output.results[0].verdict == "verified"

@pytest.mark.asyncio
async def test_section_writer_run():
    subagent = SectionWriterSubagent()
    input_data = SectionWriterInput(brief=SectionBrief(title="Introduction", objectives=["Hook reader"]))
    output = await subagent.run(input_data)
    assert output.section.title == "Introduction"
    assert "specialized subagent" in output.section.content

@pytest.mark.asyncio
async def test_citation_validator_run():
    from tools.write.models import Citation
    subagent = CitationValidatorSubagent()
    input_data = CitationValidatorInput(citations=[Citation(id="1", text="Source A", url="http://a.com")])
    output = await subagent.run(input_data)
    assert len(output.results) == 1
    assert output.results[0].is_valid == True
