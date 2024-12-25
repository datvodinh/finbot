import os
import re
from abc import ABC, abstractmethod
from urllib.parse import urljoin, urlparse

import redis
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

    def extract_all_urls(self, original_url: str, html: str) -> list:
        """
        Extract all URLs from HTML content and sort them based on relevance.

        Args:
            original_url (str): The original URL from which the HTML content was fetched.
            html (str): The HTML content to parse for URLs.

        Returns:
            list: A list of dictionaries with normalized URLs
        """
        urls = []
        base_url = urlparse(original_url)
        base_domain = f"{base_url.scheme}://{base_url.netloc}"

        soup = BeautifulSoup(html, "html.parser")
        all_urls = soup.find_all("a")

        for url in all_urls:
            href = url.get("href")
            if not href:
                continue

            # Normalize the URL
            try:
                if not href.startswith(("http://", "https://")):
                    href = urljoin(base_domain, href)

                urls.append({"href": href, "text": url.get_text().strip()})
            except Exception:
                continue

        # Sort URLs by domain match and length
        sorted_length_urls = sorted(
            urls,
            key=lambda x: (x["href"].startswith("http"), len(x["href"])),
            reverse=True,
        )

        meaningful_urls = []

        # First add same-domain URLs
        for url in sorted_length_urls:
            if base_domain in url["href"]:
                meaningful_urls.append(url)

        # Then add remaining URLs
        for url in sorted_length_urls:
            if url not in meaningful_urls:
                meaningful_urls.append(url)

        return meaningful_urls  # Return meaningful_urls instead of urls

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
