from abc import ABC, abstractmethod
from typing import List, Any


class BaseVectorStore(ABC):
    """Abstract base class for vector storage systems."""

    @abstractmethod
    async def get_client(self):
        r"""Asynchronously retrieves the client instance connected to the vector store."""
        pass

    @abstractmethod
    async def create_collection(
        self,
        collection_name: str,
        embedding_dim: int,
        **kwargs,
    ):
        r"""Asynchronously creates a new collection in the vector store with the specified name and embedding dimension."""
        pass

    @abstractmethod
    async def batch_insert(
        self,
        collection_name: str,
        points: List[Any],
        **kwargs,
    ):
        r"""Asynchronously inserts a batch of data points into the specified collection."""
        pass

    async def insert(
        self,
        collection_name: str,
        points: Any,
        **kwargs,
    ):
        r"""Asynchronously inserts a single data point into the specified collection."""
        return await self.batch_insert(
            collection_name=collection_name,
            points=[points],
            **kwargs,
        )

    @abstractmethod
    async def query(
        self,
        collection_name: str,
        query: str,
        top_k: int,
        **kwargs,
    ):
        r"""Asynchronously performs a search to find the most similar data point in the specified collection to the given query vector."""
        pass
