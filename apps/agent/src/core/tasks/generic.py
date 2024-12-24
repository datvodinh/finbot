from typing import Optional

from ..llms import OpenAIModel
from ..prompts import GENERIC
from ..types import OpenAIModelType
from .base import BaseTask


class GenericTaskExecutor(BaseTask):
    def __init__(self, model: OpenAIModelType = OpenAIModelType.GPT_4O_MINI):
        super().__init__()
        self.model = OpenAIModel(
            model=model,
        )

    async def run(
        self,
        input_query: str,
        history: Optional[list],
        **kwargs,
    ):
        return await self.model.query(
            input_query,
            history,
            system_message=GENERIC,
            **kwargs,
        )
