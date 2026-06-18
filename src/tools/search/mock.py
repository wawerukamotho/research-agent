from typing import List, Optional
import structlog
from tools.search.models import SearchQuery, SearchResult
from tools.search.base import SearchProvider

logger = structlog.get_logger()

class MockSearchProvider(SearchProvider):
    async def search(self, query: SearchQuery, namespace: str) -> List[SearchResult]:
        logger.info("mock_search_execution", query=query.query, namespace=namespace)
        return [
            SearchResult(
                title=f"Mock result {i} for {query.query} in {namespace}",
                url=f"https://example.com/{namespace}/{i}",
                snippet=f"This is a mock snippet for result {i} in the {namespace} namespace.",
                source=namespace,
                score=1.0 - (i * 0.1)
            )
            for i in range(query.limit)
        ]
