from typing import List, Type, Any
from pydantic import BaseModel
from registry.base import BaseTool
from registry.decorator import tool
from tools.search.models import SearchQuery, SearchResponse, SearchResult
from tools.search.mock import MockSearchProvider
from tools.search.base import SearchProvider

# Default provider for implementation phase
_default_provider: SearchProvider = MockSearchProvider()

class SearchToolBase(BaseTool):
    async def run(self, input_data: SearchQuery) -> SearchResponse:
        namespace = self.metadata.name
        results = await _default_provider.search(input_data, namespace)
        return SearchResponse(results=results, total_count=len(results))

@tool(
    name="web_search",
    namespace="search",
    description="Search the general web for information.",
    input_schema=SearchQuery,
    output_schema=SearchResponse
)
class WebSearchTool(SearchToolBase): pass

@tool(
    name="scholar_search",
    namespace="search",
    description="Search academic papers and scholarly articles.",
    input_schema=SearchQuery,
    output_schema=SearchResponse
)
class ScholarSearchTool(SearchToolBase): pass

@tool(
    name="arxiv_search",
    namespace="search",
    description="Search for preprints on ArXiv.",
    input_schema=SearchQuery,
    output_schema=SearchResponse
)
class ArxivSearchTool(SearchToolBase): pass

@tool(
    name="news_search",
    namespace="search",
    description="Search for current news articles.",
    input_schema=SearchQuery,
    output_schema=SearchResponse
)
class NewsSearchTool(SearchToolBase): pass

@tool(
    name="patent_search",
    namespace="search",
    description="Search for patent documents.",
    input_schema=SearchQuery,
    output_schema=SearchResponse
)
class PatentSearchTool(SearchToolBase): pass

@tool(
    name="semantic_search",
    namespace="search",
    description="Perform semantic search over indexed documents.",
    input_schema=SearchQuery,
    output_schema=SearchResponse
)
class SemanticSearchTool(SearchToolBase): pass

@tool(
    name="site_search",
    namespace="search",
    description="Search within a specific website.",
    input_schema=SearchQuery,
    output_schema=SearchResponse
)
class SiteSearchTool(SearchToolBase): pass

@tool(
    name="image_search",
    namespace="search",
    description="Search for images.",
    input_schema=SearchQuery,
    output_schema=SearchResponse
)
class ImageSearchTool(SearchToolBase): pass

@tool(
    name="video_search",
    namespace="search",
    description="Search for videos.",
    input_schema=SearchQuery,
    output_schema=SearchResponse
)
class VideoSearchTool(SearchToolBase): pass

@tool(
    name="dataset_search",
    namespace="search",
    description="Search for public datasets.",
    input_schema=SearchQuery,
    output_schema=SearchResponse
)
class DatasetSearchTool(SearchToolBase): pass

@tool(
    name="book_search",
    namespace="search",
    description="Search for books and literary works.",
    input_schema=SearchQuery,
    output_schema=SearchResponse
)
class BookSearchTool(SearchToolBase): pass

@tool(
    name="github_search",
    namespace="search",
    description="Search GitHub repositories and code.",
    input_schema=SearchQuery,
    output_schema=SearchResponse
)
class GithubSearchTool(SearchToolBase): pass

@tool(
    name="search_cache_lookup",
    namespace="search",
    description="Lookup previous search results from cache.",
    input_schema=SearchQuery,
    output_schema=SearchResponse
)
class SearchCacheLookupTool(SearchToolBase): pass

@tool(
    name="search_expand_query",
    namespace="search",
    description="Expand a search query into multiple related queries.",
    input_schema=SearchQuery,
    output_schema=SearchResponse
)
class SearchExpandQueryTool(SearchToolBase): pass
