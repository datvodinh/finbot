import os

from dotenv import load_dotenv

from src.core.types import OpenAIModelType

from ..llms import OpenAIModel
from ..prompts import SUMMARIZE
from .base import BaseTool

load_dotenv(override=True)


class SummarizeTool(BaseTool):
    def __init__(
        self,
        model: OpenAIModelType = OpenAIModelType.GPT_4O,
    ):
        super().__init__()
        self.model = OpenAIModel(
            model=model,
            base_url=os.getenv("EXTERNAL_API_BASE_URL")
            if model == OpenAIModelType.QWEN_25_32B
            else None,
        )

    async def run(self, input_query: str, history: list | None = None) -> dict:
        response = await self.model.query(
            user_message=input_query,
            system_message=SUMMARIZE % {"context": self.prepare_history(history)},
            max_completion_tokens=100,
            temperature=0,
        )

        return response.choices[0].message.content.strip()
