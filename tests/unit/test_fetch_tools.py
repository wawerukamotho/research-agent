import pytest
import httpx
from unittest.mock import patch, AsyncMock, MagicMock
from registry.registry import registry
from tools.fetch.models import FetchResponse, BatchFetchResponse

@pytest.mark.asyncio
async def test_all_fetch_tools_registered():
    import tools.fetch.tools
    fetch_tools = registry.list_tools(namespace="fetch")
    expected_tools = {
        "fetch_url", "fetch_pdf", "fetch_arxiv_paper", "fetch_wikipedia",
        "fetch_github_repo", "fetch_dataset", "fetch_rss_feed",
        "extract_main_text", "extract_tables", "extract_metadata",
        "screenshot_page", "fetch_wayback", "batch_fetch"
    }
    registered_names = {t.name for t in fetch_tools}
    assert expected_tools.issubset(registered_names)

@pytest.mark.asyncio
async def test_fetch_url_execution():
    import tools.fetch.tools
    with patch("tools.fetch.provider.httpx.AsyncClient.get") as mock_get:
        mock_response = MagicMock(spec=httpx.Response)
        mock_response.status_code = 200
        mock_response.text = "<html><body>Main content</body></html>"
        mock_response.headers = {"content-type": "text/html"}
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        result = await registry.execute("fetch.fetch_url", {"url": "https://example.com"})
        assert isinstance(result, FetchResponse)
        assert result.document.url == "https://example.com"
        assert "Main content" in result.document.content

@pytest.mark.asyncio
async def test_batch_fetch_execution():
    import tools.fetch.tools
    with patch("tools.fetch.provider.httpx.AsyncClient.get") as mock_get:
        mock_response = MagicMock(spec=httpx.Response)
        mock_response.status_code = 200
        mock_response.text = "Content"
        mock_response.headers = {"content-type": "text/plain"}
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        urls = ["https://a.com", "https://b.com"]
        result = await registry.execute("fetch.batch_fetch", {"urls": urls})
        assert isinstance(result, BatchFetchResponse)
        assert len(result.documents) == 2
        assert result.documents[0].url in urls
