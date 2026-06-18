from typing import List
from registry.base import BaseTool
from registry.decorator import tool
from tools.fetch.models import FetchInput, BatchFetchInput, FetchResponse, BatchFetchResponse, FetchedDocument
from tools.fetch.provider import DefaultFetchProvider
import httpx

_provider_instance = None

def get_fetch_provider() -> DefaultFetchProvider:
    global _provider_instance
    if _provider_instance is None:
        # This will be initialized with a pooled client in a real app flow if needed,
        # or it can remain as is for simple cases.
        _provider_instance = DefaultFetchProvider()
    return _provider_instance

class FetchToolBase(BaseTool):
    async def run(self, input_data: FetchInput) -> FetchResponse:
        provider = get_fetch_provider()
        doc = await provider.fetch(input_data.url, input_data.params)
        return FetchResponse(document=doc)

@tool(
    name="fetch_url",
    namespace="fetch",
    description="Fetch content from a generic URL.",
    input_schema=FetchInput,
    output_schema=FetchResponse
)
class FetchUrlTool(FetchToolBase): pass

@tool(
    name="fetch_pdf",
    namespace="fetch",
    description="Fetch and parse a PDF document.",
    input_schema=FetchInput,
    output_schema=FetchResponse
)
class FetchPdfTool(FetchToolBase): pass

@tool(
    name="fetch_arxiv_paper",
    namespace="fetch",
    description="Fetch a paper from ArXiv and extract its content.",
    input_schema=FetchInput,
    output_schema=FetchResponse
)
class FetchArxivPaperTool(FetchToolBase): pass

@tool(
    name="fetch_wikipedia",
    namespace="fetch",
    description="Fetch a Wikipedia article by URL or title.",
    input_schema=FetchInput,
    output_schema=FetchResponse
)
class FetchWikipediaTool(FetchToolBase): pass

@tool(
    name="fetch_github_repo",
    namespace="fetch",
    description="Fetch files or metadata from a GitHub repository.",
    input_schema=FetchInput,
    output_schema=FetchResponse
)
class FetchGithubRepoTool(FetchToolBase): pass

@tool(
    name="fetch_dataset",
    namespace="fetch",
    description="Fetch a dataset file (CSV, JSON, etc.).",
    input_schema=FetchInput,
    output_schema=FetchResponse
)
class FetchDatasetTool(FetchToolBase): pass

@tool(
    name="fetch_rss_feed",
    namespace="fetch",
    description="Fetch and parse an RSS feed.",
    input_schema=FetchInput,
    output_schema=FetchResponse
)
class FetchRssFeedTool(FetchToolBase): pass

@tool(
    name="extract_main_text",
    namespace="fetch",
    description="Extract main text content from a provided HTML string or URL.",
    input_schema=FetchInput,
    output_schema=FetchResponse
)
class ExtractMainTextTool(FetchToolBase): pass

@tool(
    name="extract_tables",
    namespace="fetch",
    description="Extract structured tables from a page.",
    input_schema=FetchInput,
    output_schema=FetchResponse
)
class ExtractTablesTool(FetchToolBase): pass

@tool(
    name="extract_metadata",
    namespace="fetch",
    description="Extract metadata (tags, author, date) from a page.",
    input_schema=FetchInput,
    output_schema=FetchResponse
)
class ExtractMetadataTool(FetchToolBase): pass

@tool(
    name="screenshot_page",
    namespace="fetch",
    description="Take a screenshot of a web page.",
    input_schema=FetchInput,
    output_schema=FetchResponse
)
class ScreenshotPageTool(FetchToolBase): pass

@tool(
    name="fetch_wayback",
    namespace="fetch",
    description="Fetch a historical version of a URL from the Wayback Machine.",
    input_schema=FetchInput,
    output_schema=FetchResponse
)
class FetchWaybackTool(FetchToolBase): pass

@tool(
    name="batch_fetch",
    namespace="fetch",
    description="Fetch multiple URLs in parallel.",
    input_schema=BatchFetchInput,
    output_schema=BatchFetchResponse
)
class BatchFetchTool(BaseTool):
    async def run(self, input_data: BatchFetchInput) -> BatchFetchResponse:
        provider = get_fetch_provider()
        docs = await provider.fetch_batch(input_data.urls)
        # Filter out exceptions if gather returned any
        valid_docs = [d for d in docs if isinstance(d, FetchedDocument)]
        return BatchFetchResponse(documents=valid_docs)
