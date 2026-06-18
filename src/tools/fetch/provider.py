from typing import List, Dict, Any
import httpx
import trafilatura
import fitz # PyMuPDF
import pandas as pd
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
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

            content_type = response.headers.get("content-type", "")

            if "application/pdf" in content_type or url.endswith(".pdf"):
                return await self.parse_pdf(url, response.content)

            content = response.text
            downloaded = trafilatura.extract(content) or content

            return FetchedDocument(
                url=url,
                content=downloaded,
                content_type=content_type,
                metadata={"status_code": response.status_code}
            )
        except Exception as e:
            raise FetchError(f"Failed to fetch {url}: {str(e)}")
        finally:
            if not self._client:
                await client.aclose()

    async def parse_pdf(self, url: str, content: bytes) -> FetchedDocument:
        try:
            doc = fitz.open(stream=content, filetype="pdf")
            text = ""
            for page in doc:
                text += page.get_text()
            return FetchedDocument(
                url=url,
                content=text,
                content_type="application/pdf",
                raw_content=content
            )
        except Exception as e:
            raise FetchError(f"Failed to parse PDF {url}: {str(e)}")

    async def screenshot(self, url: str) -> FetchedDocument:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.goto(url)
            screenshot_bytes = await page.screenshot()
            await browser.close()
            return FetchedDocument(
                url=url,
                content="Screenshot captured",
                content_type="image/png",
                raw_content=screenshot_bytes
            )

    async def extract_tables(self, url: str) -> List[Dict[str, Any]]:
        client = self._get_client()
        try:
            response = await client.get(url)
            df_list = pd.read_html(response.text)
            return [df.to_dict(orient="records") for df in df_list]
        except Exception as e:
            raise FetchError(f"Failed to extract tables from {url}: {str(e)}")

    async def fetch_batch(self, urls: List[str]) -> List[FetchedDocument]:
        import asyncio
        tasks = [self.fetch(url) for url in urls]
        return await asyncio.gather(*tasks, return_exceptions=True)
