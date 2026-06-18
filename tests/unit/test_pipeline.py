import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from registry.standard_pipelines import create_research_pipeline
from tools.search.models import SearchResponse, SearchResult
from tools.fetch.models import BatchFetchResponse, FetchedDocument
from tools.analyze.models import ClaimListResponse, Claim, VerifiedClaimListResponse, VerifiedClaim
from tools.write.models import WriteResponse

@pytest.mark.asyncio
async def test_research_pipeline_execution():
    pipeline = create_research_pipeline()

    # Mocking tool executions
    with patch("registry.registry.registry.execute") as mock_execute:
        # 1. Web Search
        mock_execute.side_effect = [
            # Search
            SearchResponse(results=[SearchResult(title="AI", url="http://ai.com", snippet="...", source="web")]),
            # Fetch
            BatchFetchResponse(documents=[FetchedDocument(url="http://ai.com", content="AI content")]),
            # Extract
            ClaimListResponse(claims=[Claim(claim="AI is good", confidence=0.9)]),
            # Cross Reference
            VerifiedClaimListResponse(verified_claims=[VerifiedClaim(
                claim="AI is good", verdict="verified", evidence=[], confidence=0.9, sources=[]
            )]),
            # Draft
            WriteResponse(content="Draft content")
        ]

        result = await pipeline.execute({"query": "AI research"})

        assert isinstance(result, WriteResponse)
        assert result.content == "Draft content"
        assert mock_execute.call_count == 5
