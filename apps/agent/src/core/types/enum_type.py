from enum import Enum


class OpenAIModelType(Enum):
    GPT_4O = "gpt-4o"
    GPT_4O_MINI = "gpt-4o-mini"
    GPT_4_TURBO = "gpt-4-turbo"
    GPT_4 = "gpt-4"
    QWEN_25_32B = "Qwen/Qwen2.5-32B-Instruct-AWQ"
