from typing import Optional, List
from dotenv import load_dotenv
from src.core.types import OpenAIModelType
from ..llms import OpenAIModel
from ..prompts import TASK_CHECK
from .base import BaseTool

load_dotenv()


class TaskCheckTool(BaseTool):
    def __init__(
        self,
        model: OpenAIModelType = OpenAIModelType.GPT_4O,
    ):
        super().__init__()
        self.model = OpenAIModel(model=model)

    async def run(
        self,
        input_query: str,
        history: Optional[List] = None,
    ) -> dict:
        response = await self.model.query(
            input_query,
            history,
            system_message=TASK_CHECK,
        )

        return self.text_to_json(
            text=response.choices[0].message.content,
        )
