from enum import Enum


class OpenAIModelType(Enum):
    GPT_4O = "gpt-4o"
    GPT_4O_MINI = "gpt-4o-mini"
    GPT_4_TURBO = "gpt-4-turbo"
    GPT_4 = "gpt-4"
    QWEN_25_32B = "Qwen/Qwen2.5-32B-Instruct-AWQ"


class OpenAIEmbeddingModelType(Enum):
    TEXT_EMBEDDING_ADA_2 = "text-embedding-ada-002"
    TEXT_EMBEDDING_3_SMALL = "text-embedding-3-small"
    TEXT_EMBEDDING_3_LARGE = "text-embedding-3-large"
    JINA_EMBEDDING = "jinaai/jina-embeddings-v3"

    @property
    def dim(self) -> int:
        if self is OpenAIEmbeddingModelType.TEXT_EMBEDDING_ADA_2:
            return 1536
        elif self is OpenAIEmbeddingModelType.TEXT_EMBEDDING_3_SMALL:
            return 1536
        elif self is OpenAIEmbeddingModelType.TEXT_EMBEDDING_3_LARGE:
            return 3072
        elif self is OpenAIEmbeddingModelType.JINA_EMBEDDING:
            return 1024


class TaskType:
    GENERIC = "generic"
    SCRAPE = "scrape"
    SEARCH = "search"

    @staticmethod
    def is_generic_task(task: str) -> str:
        """Check if the given task is a generic task."""
        if task in [TaskType.SCRAPE, TaskType.SEARCH]:
            return False
        return True
