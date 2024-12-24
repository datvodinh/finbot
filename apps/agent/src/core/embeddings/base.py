from abc import ABC, abstractmethod
from typing import Any, List


class BaseEmbedding(ABC):
    @abstractmethod
    async def batch_embed(
        self, nodes: list[str], **kwargs: Any
    ) -> List[List[float]]:
        """Abstract method for embedding a list of text strings into a list of numerical vectors."""
        pass

    async def embed(
        self,
        node: str,
        **kwargs: Any,
    ) -> List[float]:
        r"""Generates an embedding for the given text."""
        embeddings = await self.batch_embed([node], **kwargs)
        return embeddings[0]

    @abstractmethod
    async def get_embedding_dim(self) -> int:
        r"""Returns the embedding dimension of the embeddings."""
        pass
