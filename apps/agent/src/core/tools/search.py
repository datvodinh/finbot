import os
from typing import List

from dotenv import load_dotenv
from googleapiclient.discovery import build

from .base import BaseTool

load_dotenv()


class SearchTool(BaseTool):
    def __init__(self):
        super().__init__()

    async def run(
        self,
        query: str,
        num_results=5,
    ) -> List[str]:
        # Build the custom search service
        service = build(
            serviceName="customsearch",
            version="v1",
            developerKey=os.getenv("GOOGLE_API_KEY"),
        )

        # Perform the search
        results = []
        try:
            response = (
                service.cse()
                .list(
                    q=query,
                    cx=os.getenv("GOOGLE_CSE_ID"),
                    num=num_results,
                )
                .execute()
            )
            if "items" in response:
                for item in response["items"]:
                    # Collect the URLs from search results
                    if ".pdf" not in item["link"]:
                        results.append(item["link"])
        except Exception as e:
            print(f"An error occurred: {e}")

        return results
