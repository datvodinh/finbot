import json
from typing import Dict, List, Literal

import httpx
from playwright.async_api import TimeoutError, async_playwright
from rich.console import Console

from .base import BaseCrawler

console = Console()


class HtmlCrawler(BaseCrawler):
    def __init__(self, config: dict = {}):
        """
        Crawler for HTML content.

        Args:
            config (dict, optional): Configuration for the crawler.
            ```python
            - headers (dict, optional): Headers for the request. Defaults to BASE_HEADERS.
            - headless (bool, optional): Headless mode for the browser. Defaults to True.
            - timeout (int, optional): Timeout for the browser. Defaults to 60000 (60 seconds).
            - end_with_capture (bool, optional): Take a screenshot before closing the browser. Defaults to False.
            - fetch_strategy (str, optional): Fetch strategy: requests or browser or hybrid. Defaults to hybrid.
            - max_recursive_depth (int, optional): Recursively fetch urls depth. Defaults to 0.
            - max_recursive_urls (int, optional): Maximum number of urls to recursively fetch. Defaults to 5.
            - cache_ttl (int, optional): Cache TTL. Defaults to 600.
            ```
        """
        super().__init__(config)

        self.headers = self.config.get("headers", self.base_headers)
        self.headless = self.config.get("headless", True)
        self.timeout = self.config.get("timeout", 60000)
        self.cache_ttl = self.config.get("cache_ttl", 600)
        self.end_with_capture = self.config.get("end_with_capture", False)
        self.fetch_strategy = self.config.get("fetch_strategy", "hybrid")
        self.max_recursive_depth = self.config.get("max_recursive_depth", 0)
        self.max_recursive_urls = self.config.get("max_recursive_urls", 5)

    async def _fetch_by_requests(
        self, url: str
    ) -> dict[
        Literal["markdown", "urls"], str | list[dict[Literal["href", "text"], str]]
    ]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(url, headers=self.headers)
            response.raise_for_status()
            return {
                "markdown": self.markdownify(html=response.text),
                "urls": self.extract_all_urls(original_url=url, html=response.text),
            }

    async def _fetch_by_browser(
        self, url: str
    ) -> dict[
        Literal["markdown", "urls"], str | list[dict[Literal["href", "text"], str]]
    ]:
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=self.headless,
                timeout=self.timeout,
            )
            page = await browser.new_page()

            await page.set_extra_http_headers(self.headers)

            try:
                await page.goto(url)
            except TimeoutError:
                print("Timeout reached, collecting available data")
            finally:
                if self.end_with_capture:
                    await page.screenshot(path="screenshot.png")

            # Get content of the page, then convert to markdown
            content = await page.content()
            await browser.close()

            return {
                "markdown": self.markdownify(content),
                "urls": self.extract_all_urls(content),
            }

    async def fetch(self, url: str) -> List[Dict[str, str]]:
        if self.fetch_strategy == "requests":
            data = await self._fetch_by_requests(url)
        elif self.fetch_strategy == "browser":
            data = await self._fetch_by_browser(url)
        elif self.fetch_strategy == "hybrid":
            try:
                data = await self._fetch_by_requests(url)
                console.print("[bold cyan]Fetched by requests[/bold cyan]")
            except httpx.HTTPStatusError:
                data = await self._fetch_by_browser(url)
                console.print("[bold magenta]Fetched by browser[/bold magenta]")
        else:
            raise ValueError(f"Invalid fetch strategy: {self.fetch_strategy}")

        return data

    async def run(self, url: str) -> dict[Literal["context"]]:
        # TODO: Check cached, then search Qdrant for similar data. Update below part:

        ######################################################
        cached_data = self.cache_db.get(url)

        if cached_data is not None:
            print("CACHE HIT: {}".format(url))
            return json.loads(cached_data.decode("utf-8"))
        ######################################################

        # Firsts fetch
        data = await self.fetch(url)

        if self.max_recursive_depth > 0:
            pass

        # TODO: Chunking then storing data in Qdrant for later use. Set cached and ttl for crawled data. Update below part:

        ######################################################
        self.cache_db.set(
            url,
            json.dumps(data, indent=2, ensure_ascii=False),
            ex=self.cache_ttl,
        )

        return data
        ######################################################
