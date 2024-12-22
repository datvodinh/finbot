from src.core.types import OpenAIModelType

from ..llms import OpenAIModel
from ..prompts import SUMMARIZE
from .base import BaseTool


class SummarizeTool(BaseTool):
    def __init__(
        self,
        model: OpenAIModelType = OpenAIModelType.GPT_4O_MINI,
    ):
        super().__init__()
        self.model = OpenAIModel(model=model)

    async def run(self, input_query: str, history: list | None = None) -> dict:
        response = await self.model.query(
            input_query,
            history,
            system_message=SUMMARIZE,
        )

        return self.text_to_json(response.choices[0].message.content)
