import asyncio
from typing import List

from apps.crawler import HtmlCrawler

from .base import BaseTool


class FetchUrlsTool(BaseTool):
    def __init__(self, config: dict = {}):
        super().__init__()
        self.crawler = HtmlCrawler(config=config)

    async def run(self, urls: List[str]) -> str:
        tasks = [self.crawler.run(url) for url in urls]

        # A dictionary of urls and their respective markdown content
        data = dict(zip(urls, await asyncio.gather(*tasks)))

        output = ""

        for url, content in data.items():
            output += (
                f"## Below is the content of website with url: {url}\n{content}\n\n"
            )

        return output
