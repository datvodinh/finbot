from openai import AsyncOpenAI
from dotenv import load_dotenv
from src.core.embeddings.base import BaseEmbedding
from src.core.types import (
    OpenAIEmbeddingModelType,
)
from typing import Any, List

load_dotenv()


class OpenAIEmbedding(BaseEmbedding):
    def __init__(
        self,
        model: OpenAIEmbeddingModelType = OpenAIEmbeddingModelType.TEXT_EMBEDDING_3_LARGE,
    ):
        """Initializes an instance of the OpenAIEmbedding class."""
        super().__init__()
        self.client = AsyncOpenAI(
            timeout=120,
            max_retries=3,
            base_url="http://localhost:8000/v1"
            if model == OpenAIEmbeddingModelType.JINA_EMBEDDING
            else None,
        )
        self.model_type = model

    async def batch_embed(
        self,
        nodes: List[str],
        **kwargs: Any,
    ) -> List[List[float]]:
        """Asynchronously generates embeddings for a list of text strings using the OpenAI API."""
        response = await self.client.embeddings.create(
            input=nodes,
            model=self.model_type.value,
            dimensions=self.model_type.dim,
            **kwargs,
        )
        return [data.embedding for data in response.data]

    async def get_embedding_dim(self) -> int:
        """Asynchronously retrieves the embedding dimension of the current model."""
        return self.model_type.dim
