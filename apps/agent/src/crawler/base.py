import os
import re
import redis
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from markdownify import markdownify as md

from ..shared import const

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

    def extract_all_urls(self, html: str) -> list:
        """
        Extract all urls from html content
        """
        urls = []

        soup = BeautifulSoup(html, "html.parser")
        all_urls = soup.find_all("a")

        for url in all_urls:
            urls.append(
                {
                    "href": url.get("href"),
                    "text": url.get_text(),
                }
            )

        return urls

    def markdownify(self, html: str) -> str:
        """
        Convert html to markdown
        """
        result = md(html)

        if not result:
            return "N/A"

        # Remove markdown links while keeping the text
        # Changes [text](url) to just text

        result = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", result)

        # Remove multiple newlines/spaces
        result = re.sub(
            r"\n{3,}", "\n\n", result
        )  # Replace 3+ newlines with 2
        result = re.sub(
            r" {2,}", " ", result
        )  # Replace multiple spaces with single

        # Remove empty lines at start/end
        result = result.strip()

        # Remove empty bullet points and their newlines
        result = re.sub(r"\n\s*[-*+]\s*\n", "\n", result)

        # Remove URLs that may be left plain in the text
        result = re.sub(
            r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
            "",
            result,
        )

        # Remove any remaining empty lines
        result = re.sub(r"^\s*$\n", "", result, flags=re.MULTILINE)

        # Normalize whitespace between sections
        result = re.sub(r"\n{3,}", "\n\n", result)

        return result.strip()

    @abstractmethod
    async def run(self) -> str:
        """
        Fetch data and return the markdown content converted from the html
        """
        pass
