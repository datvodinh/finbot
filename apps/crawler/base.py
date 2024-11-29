import os
from abc import ABC, abstractmethod

import redis
from dotenv import load_dotenv
from markdownify import markdownify as md

from apps.shared import const

load_dotenv(override=True)


class BaseCrawler(ABC):
    def __init__(self, config: dict = {}):
        self.config = config
        self.base_headers = const.BASE_HEADERS

        self.cache_db = redis.Redis(
            host=os.getenv("REDIS_HOST"),
            port=os.getenv("REDIS_PORT"),
            db=os.getenv("REDIS_DB"),
        )
        self.cache_db.ping()
        self.cache_ttl = const.CACHE_TTL

    def markdownify(self, html: str) -> str:
        """
        Convert html to markdown
        """
        result = md(html)

        if not result:
            return "N/A"

        # If 3 newlines consecutively, replace with 2 newlines
        return result.replace("\n\n\n", "\n\n")

    @abstractmethod
    async def run(self) -> str:
        """
        Fetch data and return the markdown content converted from the html
        """
        pass
