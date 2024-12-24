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

    @property
    def dim(self) -> int:
        if self is OpenAIEmbeddingModelType.TEXT_EMBEDDING_ADA_2:
            return 1536
        elif self is OpenAIEmbeddingModelType.TEXT_EMBEDDING_3_SMALL:
            return 1536
        elif self is OpenAIEmbeddingModelType.TEXT_EMBEDDING_3_LARGE:
            return 3072
