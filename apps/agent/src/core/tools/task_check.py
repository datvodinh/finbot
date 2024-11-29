from src.core.types import OpenAIModelType

from ..llms import OpenAIModel
from ..prompts import TASK_CHECK
from .base import BaseTool


class TaskCheckTool(BaseTool):
    def __init__(
        self,
        model: OpenAIModelType = OpenAIModelType.GPT_4O,
    ):
        super().__init__()
        self.model = OpenAIModel(model=model)

    async def run(self, input_query: str, history: list | None = None) -> dict:
        response = await self.model.query(
            input_query,
            history,
            system_message=TASK_CHECK,
        )

        return self.text_to_json(response.choices[0].message.content)
