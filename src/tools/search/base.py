from abc import ABC, abstractmethod
from typing import List
from tools.search.models import SearchQuery, SearchResult

class SearchProvider(ABC):
    @abstractmethod
    async def search(self, query: SearchQuery, namespace: str) -> List[SearchResult]:
        pass
