import uuid
import tiktoken
from typing import Any, Dict, List, Optional, Union
from qdrant_client import AsyncQdrantClient, models
from qdrant_client.http.models import Distance, VectorParams
from src.core.embeddings import OpenAIEmbedding
from src.core.types import OpenAIEmbeddingModelType
from src.core.vectordb.base import BaseVectorStore


class QdrantVectorStore(BaseVectorStore):
    def __init__(
        self,
        location: str = "http://localhost:6333",
        collection_name: str = "finbot",
        model_type: OpenAIEmbeddingModelType = OpenAIEmbeddingModelType.TEXT_EMBEDDING_3_LARGE,
    ) -> None:
        super().__init__()
        self.location = location
        self.model_type = model_type
        self.model = OpenAIEmbedding(model=self.model_type)
        self.encoding = tiktoken.encoding_for_model("gpt-4o-mini")
        self.collection_name = collection_name

    async def get_client(self) -> AsyncQdrantClient:
        """Asynchronously retrieves an AsyncQdrantClient connected to the specified location."""
        return AsyncQdrantClient(location=self.location)

    async def create_collection(self) -> bool:
        """Asynchronously creates a new collection in Qdrant if it does not already exist."""
        client = await self.get_client()
        if await client.collection_exists(self.collection_name):
            return
        return await client.create_collection(
            collection_name=self.collection_name,
            vectors_config={
                "text": VectorParams(
                    size=self.model_type.dim,
                    distance=Distance.COSINE,
                )
            },
        )

    def _get_text(
        self,
        point: Dict[str, Any],
        embedding_keys: Optional[List[str]],
    ):
        """Extracts the text from the given point."""
        text = ""
        if embedding_keys is None:
            return point["text"]

        for key in embedding_keys:
            header = key if key != "text" else "content"
            if point[key] is not None:
                text += f"{header.upper()}: {point[key]}\n"
        return text

    async def _get_embedding(
        self,
        points: List[Dict[str, Any]],
        embedding_keys: Optional[List[str]],
    ) -> List[List[float]]:
        """Asynchronously retrieves embeddings for the given points."""
        texts = [self._get_text(point, embedding_keys) for point in points]
        embeddings = await self.model.batch_embed(texts)
        return embeddings, texts

    def _get_payload(
        self,
        point: Union[str, Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Generates a payload dictionary from the given point."""
        if isinstance(point, str):
            return {"text": point}

        return point

    def _get_uuid(
        self,
        point: Union[str, Dict[str, Any]],
    ) -> str:
        """Generates a unique UUID based on the content of the given point."""
        if isinstance(point, str):
            text = point
        else:
            text = point["text"]
        return str(uuid.uuid5(uuid.NAMESPACE_DNS, text))

    def _chunk(
        self,
        points: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """Chunks the points into smaller pieces if the encoded text is too long."""
        chunk_points = []
        for point in points:
            encode = self.encoding.encode(point["text"])
            if len(encode) > 2048:
                point.pop("text")
                metadata = point.copy()

                for idx in range(0, len(encode), 2048):
                    new_point = {
                        "text": encode[idx : idx + 2048],
                        **metadata,
                    }
                    chunk_points.append(new_point)
            else:
                chunk_points.append(point)

    async def _delete_points_with_urls(
        self,
        urls: List[str],
    ):
        """Delete points with the URL(s), if the URL(s) expired in Redis."""
        client = await self.get_client()
        await client.delete(
            collection_name="{collection_name}",
            points_selector=models.FilterSelector(
                filter=models.Filter(
                    must=[
                        models.FieldCondition(
                            key="url",
                            match=models.MatchAny(any=urls),
                        ),
                    ],
                )
            ),
        )

    async def batch_insert(
        self,
        collection_name: str,
        points: List[Dict[str, Any]],
        embedding_keys: Optional[List[str]] = ["text"],
        **kwargs,
    ) -> None:
        """Asynchronously inserts multiple points into the specified collection."""

        assert all(
            isinstance(point, dict) for point in points
        ), "All points should be dictionary"

        assert all(
            "text" in point for point in points
        ), "All points should have 'text' key"

        if embedding_keys is not None:
            assert all(
                [key in point for key in embedding_keys for point in points]
            ), f"Redundant keys in the embedding_keys: {embedding_keys}"
        
        # Chunk the points if the encoded text is too long
        points = self._chunk(points)
        
        # Remove points with expired URLs
        urls = list(map(lambda point: point["url"], points))
        await self._delete_points_with_urls(urls)

        client = await self.get_client()
        if not await client.collection_exists(collection_name):
            await self.create_collection(collection_name)
        embeddings, texts = await self._get_embedding(points, embedding_keys)

        point_list = models.PointsList(
            points=[
                models.PointStruct(
                    id=self._get_uuid(text),
                    vector={
                        "text": embedding,
                    },
                    payload=self._get_payload(point),
                )
                for point, embedding, text in zip(points, embeddings, texts)
            ]
        )

        await client.upsert(
            collection_name=collection_name,
            points=point_list,
            **kwargs,
        )

    async def query(
        self,
        collection_name: str,
        query: str,
        top_k: int = 6,
        filters: Optional[models.Filter] = None,
        **kwargs,
    ) -> List[models.ScoredPoint]:
        """Asynchronously queries the specified collection for similar embeddings to the given query."""
        collection_name = collection_name.lower()
        client = await self.get_client()
        if not await client.collection_exists(collection_name):
            raise ValueError(f"Collection {collection_name} does not exist.")

        embedding = await self.model.embed(query)

        response = await client.search(
            collection_name=collection_name,
            query_vector=models.NamedVector(
                name="text",
                vector=embedding,
            ),
            limit=top_k,
            query_filter=filters,
            **kwargs,
        )

        return response
