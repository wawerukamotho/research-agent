import pytest
from unittest.mock import patch, AsyncMock
from registry.registry import registry
from tools.analyze.models import AnalysisResponse, ClaimListResponse

@pytest.mark.asyncio
async def test_all_analyze_tools_registered():
    import tools.analyze.tools
    analyze_tools = registry.list_tools(namespace="analyze")
    expected_tools = {
        "summarize_text", "extract_claims", "cross_reference_claims",
        "score_source_credibility", "detect_contradictions", "extract_entities",
        "compute_topic_coverage", "rank_sources", "identify_knowledge_gaps",
        "classify_claim_type", "timeline_extract", "sentiment_analysis",
        "compare_sources"
    }
    registered_names = {t.name for t in analyze_tools}
    assert expected_tools.issubset(registered_names)

@pytest.mark.asyncio
async def test_summarize_text_execution():
    import tools.analyze.tools
    with patch("tools.analyze.provider.litellm.acompletion") as mock_completion:
        mock_completion.return_value = AsyncMock(
            choices=[
                AsyncMock(
                    message=AsyncMock(
                        content='{"summary": "A brief summary of AI agents.", "claims": [], "entities": [], "metadata": {}}'
                    )
                )
            ]
        )

        result = await registry.execute("analyze.summarize_text", {"text": "Long text about AI agents..."})
        assert isinstance(result, AnalysisResponse)
        assert result.summary == "A brief summary of AI agents."

@pytest.mark.asyncio
async def test_extract_claims_execution():
    import tools.analyze.tools
    with patch("tools.analyze.provider.litellm.acompletion") as mock_completion:
        mock_completion.return_value = AsyncMock(
            choices=[
                AsyncMock(
                    message=AsyncMock(
                        content='{"claims": [{"claim": "AI is fast", "confidence": 0.9}]}'
                    )
                )
            ]
        )

        result = await registry.execute("analyze.extract_claims", {"text": "AI technology is rapidly advancing."})
        assert isinstance(result, ClaimListResponse)
        assert len(result.claims) == 1
        assert result.claims[0].claim == "AI is fast"
