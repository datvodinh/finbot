import asyncio
import json
from typing import Dict, List

import httpx
from playwright.async_api import TimeoutError, async_playwright
from rich.console import Console

from .base import BaseCrawler

console = Console()


class HtmlCrawler(BaseCrawler):
    def __init__(self, config: dict):
        super().__init__(config)

        self.headers = self.config.get("headers", self.base_headers)
        self.headless = self.config.get("headless", True)
        self.timeout = self.config.get("timeout", 10000)
        self.cache_ttl = self.config.get("cache_ttl", 600)
        self.end_with_capture = self.config.get("end_with_capture", False)
        self.fetch_strategy = self.config.get("fetch_strategy", "hybrid")
        self.max_recursive_urls = self.config.get("max_recursive_urls", 6)

    async def _fetch_by_requests(self, url: str) -> str:
        print(f"==>> url: {url}")
        try:
            async with httpx.AsyncClient(
                timeout=5,
                max_redirects=0,
            ) as client:
                response = await client.get(url, headers=self.headers)
                response.raise_for_status()
                return {
                    "markdown": self.markdownify(response.text),
                    "urls": self.extract_all_urls(response.text),
                }
        except Exception as _:
            return {
                "markdown": "",
                "urls": [],
            }

    async def _fetch_by_browser(self, url: str) -> str:
        print(f"==>> url: {url}")
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=self.headless,
                timeout=self.timeout,
            )

            try:
                page = await browser.new_page()

                # Set header for page
                await page.set_extra_http_headers(self.headers)
                await page.goto(url)
                content = await page.content()
                return {
                    "markdown": self.markdownify(content),
                    "urls": self.extract_all_urls(content),
                }
            except TimeoutError:
                print("Timeout reached, collecting available data")
                return {
                    "markdown": "",
                    "urls": [],
                }
            finally:
                if self.end_with_capture:
                    await page.screenshot(path="screenshot.png")
                await browser.close()

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

    async def run(self, url: str) -> str:
        # Check cache first
        cached_data = self.cache_db.get(url)

        if cached_data is not None:
            print("CACHE HIT: {}".format(url))
            return json.loads(cached_data.decode("utf-8"))

        # Firsts fetch
        data = await self.fetch(url)

        urls = data.get("urls", [])

        tasks = [self.fetch(url) for url in urls[: self.max_recursive_urls]]

        first_depth_data = await asyncio.gather(*tasks)

        total_markdown = (
            data["markdown"]
            + "\n\n"
            + "\n\n".join([d["markdown"] for d in first_depth_data])
        )

        data["markdown"] = total_markdown

        # Cache the data
        self.cache_db.set(
            url,
            json.dumps(data, indent=2, ensure_ascii=False),
            ex=self.cache_ttl,
        )

        return data
