from typing import Any, Dict, List, Optional

from src.core.tasks import GenericTaskExecutor, RAGTaskExecutor
from src.core.tools import FetchUrlsTool, TaskCheckTool
from src.core.types import OpenAIModelType


class FinDAgent:
    def __init__(
        self,
    ) -> None:
        """Initialize the FinDAgent."""
        super().__init__()

        self._task_check_tool = TaskCheckTool(
            model=OpenAIModelType.GPT_4O,
        )

        self._generic_task = GenericTaskExecutor(
            model=OpenAIModelType.GPT_4O,
        )

        self._fetch_urls_tool = FetchUrlsTool()

        self._rag_task = RAGTaskExecutor(
            model=OpenAIModelType.GPT_4O,
        )

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

        print("Task check result:", result)

        context = ""

        if result["task"] == "generic":
            response = await self._generic_task.run(
                input_query=user_message,
                history=history,
                **kwargs,
            )
        elif result["task"] == "scrape_web_content":
            context: str = await self._fetch_urls_tool.run(
                urls=result["urls"],
            )

            response = await self._rag_task.run(
                input_query=user_message,
                context=context,
                history=history,
                **kwargs,
            )
        else:
            raise NotImplementedError(f"Task {result['task']} is not implemented")

        yield response
