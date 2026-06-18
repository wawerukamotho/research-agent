from typing import List, Dict, Any
import httpx
import trafilatura
from tools.fetch.base import FetchProvider
from tools.fetch.models import FetchedDocument
from scaffold.errors import FetchError

class DefaultFetchProvider(FetchProvider):
    def __init__(self, client: httpx.AsyncClient = None):
        self._client = client

    def _get_client(self) -> httpx.AsyncClient:
        if self._client:
            return self._client
        # Fallback for tests or when not running in FastAPI context
        return httpx.AsyncClient(follow_redirects=True)

    async def fetch(self, url: str, params: Dict[str, Any] = None) -> FetchedDocument:
        client = self._get_client()
        try:
            response = await client.get(url, params=params)
            if hasattr(response, "raise_for_status"):
                response.raise_for_status()

            content = response.text
            downloaded = trafilatura.extract(content) or content

            return FetchedDocument(
                url=url,
                content=downloaded,
                content_type=response.headers.get("content-type", "text/html"),
                metadata={"status_code": response.status_code}
            )
        except Exception as e:
            raise FetchError(f"Failed to fetch {url}: {str(e)}")
        finally:
            if not self._client:
                await client.aclose()

    async def fetch_batch(self, urls: List[str]) -> List[FetchedDocument]:
        import asyncio
        tasks = [self.fetch(url) for url in urls]
        return await asyncio.gather(*tasks, return_exceptions=True)
