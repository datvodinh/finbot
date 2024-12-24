import os
import asyncio
import time
from typing import Any, Dict, List, Optional
from src.core.tasks import GenericTaskExecutor, RAGTaskExecutor
from src.core.tools import FetchUrlsTool, TaskCheckTool, SearchTool
from src.core.types import OpenAIModelType, TaskType
from src.core.vectordb import QdrantVectorStore


class FinBotAgent:
    def __init__(
        self,
    ) -> None:
        """Initialize the FinBotAgent."""
        super().__init__()

        self._task_check_tool = TaskCheckTool(
            model=OpenAIModelType.GPT_4O,
        )

        self._generic_task = GenericTaskExecutor(
            model=OpenAIModelType.GPT_4O_MINI,
        )

        self._fetch_urls_tool = FetchUrlsTool()

        self._search_tool = SearchTool()

        self._rag_task = RAGTaskExecutor(
            model=OpenAIModelType.GPT_4O_MINI,
        )

        self._vector_store = QdrantVectorStore(
            location=os.getenv("QDRANT_URL", "http://localhost:6333"),
        )

        asyncio.run(self._vector_store.create_collection())

    async def _check_task(
        self,
        input_query: str,
        history: Optional[List[Dict[str, Any]]] = None,
    ) -> dict:
        """Determine the intention behind the user's input query."""
        return await self._task_check_tool.run(
            input_query=input_query,
            history=history,
        )

    async def chat(
        self,
        user_message: str,
        history: Optional[list] = None,
        **kwargs,
    ):
        """Handle a user message and generate a response."""

        result = await self._check_task(
            input_query=user_message,
            history=history,
        )

        yield {
            "action": "task_check",
            "content": result["task"],
        }

        if TaskType.is_generic_task(result["task"]):
            response = await self._generic_task.run(
                input_query=user_message,
                history=history,
                **kwargs,
            )
        else:
            yield {
                "action": "search",
                "content": f"🔍 Searching for information about '{user_message}'...",
            }

            if result["task"] == TaskType.SEARCH:
                urls = await self._search_tool.run(
                    query=user_message,
                    num_results=3,
                )
                yield {
                    "action": "search_urls",
                    "content": urls,
                }
            else:
                urls = result["urls"]
                yield {
                    "action": "fetch_urls",
                    "content": urls,
                }

            start_time = time.perf_counter()
            data: List[Dict[str, str]] = await self._fetch_urls_tool.run(
                urls=urls,
            )
            time_elapsed = time.perf_counter() - start_time

            yield {
                "action": "crawl_urls",
                "content": f"🕒 Fetched these URLs in {time_elapsed:.2f} seconds.",
            }

            await self._vector_store.batch_insert(
                points=data,
                embedding_keys=list(data[0].keys()),
            )

            yield {
                "action": "vector_store",
                "content": "📦 Stored the fetched URLs in the vector store.",
            }

            context = await self._vector_store.query(
                query=user_message,
                top_k=10,
            )

            response = await self._rag_task.run(
                input_query=user_message,
                context=context,
                history=history,
                **kwargs,
            )

        yield {
            "action": "answer",
            "content": response,
        }
