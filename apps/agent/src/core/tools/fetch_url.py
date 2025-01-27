import asyncio
from datetime import datetime
from typing import Dict, List
from .base import BaseTool
from ..crawler import HtmlCrawler


class FetchUrlsTool(BaseTool):
    def __init__(self, config: dict = {}):
        super().__init__()
        self.crawler = HtmlCrawler(config=config)

    async def run(
        self,
        urls: List[str],
        recursive: bool = False,
    ) -> List[Dict[str, str]]:
        urls = [url for url in urls if ".pdf" not in url]
        tasks = [self.crawler.run(url, recursive=recursive) for url in urls]

        # A dictionary of urls and their respective markdown content
        data = dict(zip(urls, await asyncio.gather(*tasks)))

        points = []

        for url, content in data.items():
            points.append(
                {
                    "url": url,
                    "text": content["markdown"],
                    "status": content["status"],
                    "timestamp": datetime.now().strftime(
                        "%d-%m-%Y at %I:%M %p"
                    ),
                }
            )
        return points
