from abc import ABC, abstractmethod
from typing import List, Dict, Any
from tools.fetch.models import FetchedDocument, FetchInput

class FetchProvider(ABC):
    @abstractmethod
    async def fetch(self, url: str, params: Dict[str, Any] = None) -> FetchedDocument:
        pass

    @abstractmethod
    async def fetch_batch(self, urls: List[str]) -> List[FetchedDocument]:
        pass
