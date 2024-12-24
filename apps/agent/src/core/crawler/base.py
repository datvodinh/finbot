import os
import re
from abc import ABC, abstractmethod

import redis
import tldextract
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from markdownify import markdownify as md
from qdrant_client import AsyncQdrantClient, models

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

        self.qdrant = AsyncQdrantClient(
            host=os.getenv("QDRANT_HOST"),
            port=os.getenv("QDRANT_PORT"),
        )

    async def create_collection(self):
        if not await self.qdrant.collection_exists(
            os.getenv("QDRANT_COLLECTION", "finbot")
        ):
            await self.qdrant.create_collection(
                collection_name=os.getenv("QDRANT_COLLECTION", "finbot"),
                vectors_config={
                    "text": models.VectorParams(
                        size=1024,
                        distance=models.Distance.COSINE,
                    ),
                },
            )

    def extract_all_urls(self, original_url: str, html: str) -> list:
        """
        Extract all URLs from HTML content and sort them based on relevance.

        This method parses the provided HTML content to find all anchor tags (<a>),
        extracts their href attributes and text content, and returns a list of URLs.
        The URLs are sorted such that those with the same domain as the original URL
        and longer in length are considered more meaningful and are prioritized.

        Args:
            original_url (str): The original URL from which the HTML content was fetched.
            html (str): The HTML content to parse for URLs.

        Returns:
            list: A list of dictionaries, each containing 'href' and 'text' keys representing
                  the URL and its associated text content, respectively.
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

        # Urls with the same domain and longer in length should be more meaningful to recursively fetch
        sorted_length_urls = sorted(
            urls,
            key=lambda x: (x["href"].startswith("http"), len(x["href"])),
            reverse=True,
        )

        meaningful_urls = []

        extracted = tldextract.extract(original_url)
        root_domain_original_url = f"{extracted.domain}.{extracted.suffix}"

        for url in sorted_length_urls:
            # Check the same domain
            if root_domain_original_url in url["href"]:
                meaningful_urls.append(url)

        # Add the rest
        for url in sorted_length_urls:
            if url not in meaningful_urls:
                meaningful_urls.append(url)

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
        result = re.sub(r"\n{3,}", "\n\n", result)  # Replace 3+ newlines with 2
        result = re.sub(r" {2,}", " ", result)  # Replace multiple spaces with single

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
