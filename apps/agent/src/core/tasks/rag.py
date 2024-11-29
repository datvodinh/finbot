from typing import Optional

from ..llms import OpenAIModel
from ..prompts import RAG
from ..types import OpenAIModelType
from .base import BaseTask


class RAGTaskExecutor(BaseTask):
    def __init__(self, model: OpenAIModelType = OpenAIModelType.GPT_4O):
        super().__init__()
        self.model = OpenAIModel(
            model=model,
        )

    async def run(
        self,
        input_query: str,
        context: str,
        history: Optional[list] = None,
        **kwargs,
    ):
        return await self.model.query(
            input_query,
            history=history,
            system_message=RAG.format(context=context),
            **kwargs,
        )
