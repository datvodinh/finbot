import httpx
from playwright.async_api import TimeoutError, async_playwright

from .base import BaseCrawler


class HtmlCrawler(BaseCrawler):
    def __init__(self, config: dict = {}):
        super().__init__(config)

        self.headers = self.config.get("headers", self.base_headers)
        self.headless = self.config.get("headless", True)
        self.timeout = self.config.get("timeout", 60000)

        # Before the browser closes, take a screenshot or not
        self.end_with_capture = self.config.get("end_with_capture", False)

        # Fetch strategy: requests or browser or hybrid (default: hybrid)
        self.fetch_strategy = self.config.get("fetch_strategy", "hybrid")

    async def fetch_by_requests(self, url: str) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)
            response.raise_for_status()
            return self.markdownify(response.text)

    async def fetch_by_browser(self, url: str) -> str:
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=self.headless,
                timeout=self.timeout,
            )
            page = await browser.new_page()

            # Set header for page
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
            return self.markdownify(content)

    async def run(self, url: str) -> str:
        # Check cache first
        cached_data = self.cache_db.get(url)

        if cached_data is not None:
            print("CACHE HIT: {}".format(url))
            return cached_data.decode("utf-8")

        if self.fetch_strategy == "requests":
            data = await self.fetch_by_requests(url)
        elif self.fetch_strategy == "browser":
            data = await self.fetch_by_browser(url)
        elif self.fetch_strategy == "hybrid":
            try:
                data = await self.fetch_by_requests(url)
                print("Fetched by requests")
            except httpx.HTTPStatusError:
                data = await self.fetch_by_browser(url)
                print("Fetched by browser")
        else:
            raise ValueError("Invalid fetch strategy: {}".format(self.fetch_strategy))

        # Cache the data
        self.cache_db.set(url, data, ex=self.cache_ttl)

        return data
