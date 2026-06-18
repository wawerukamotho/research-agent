import pytest
from registry.registry import registry
from tools.search.models import SearchQuery, SearchResponse

@pytest.mark.asyncio
async def test_all_search_tools_registered():
    import tools.search.tools
    search_tools = registry.list_tools(namespace="search")
    expected_tools = {
        "web_search", "scholar_search", "arxiv_search", "news_search",
        "patent_search", "semantic_search", "site_search", "image_search",
        "video_search", "dataset_search", "book_search", "github_search",
        "search_cache_lookup", "search_expand_query"
    }
    registered_names = {t.name for t in search_tools}
    assert expected_tools.issubset(registered_names)

@pytest.mark.asyncio
async def test_web_search_execution():
    # Make sure tools are registered
    import tools.search.tools

    result = await registry.execute("search.web_search", {"query": "AI agents", "limit": 5})
    assert isinstance(result, SearchResponse)
    assert len(result.results) == 5
    assert "AI agents" in result.results[0].title
    assert result.results[0].source == "web_search"

@pytest.mark.asyncio
async def test_arxiv_search_execution():
    import tools.search.tools

    result = await registry.execute("search.arxiv_search", {"query": "transformer models", "limit": 2})
    assert isinstance(result, SearchResponse)
    assert len(result.results) == 2
    assert "transformer models" in result.results[0].title
    assert result.results[0].source == "arxiv_search"
