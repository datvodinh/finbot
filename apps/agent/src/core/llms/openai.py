from typing import Optional

from dotenv import load_dotenv
from openai import AsyncOpenAI

from src.core.llms.base import BaseModel
from src.core.prompts import CHAT_PROMPT_EN
from src.core.types import (
    OpenAIModelType,
)

load_dotenv(override=True)


class OpenAIModel(BaseModel):
    def __init__(
        self,
        model: OpenAIModelType = OpenAIModelType.GPT_4O_MINI,
        base_url: Optional[str] = None,
    ):
        r"""Initializes an instance of the OpenAIModel class."""
        super().__init__()
        self.client = AsyncOpenAI(
            timeout=120,
            max_retries=3,
            base_url=base_url,
        )

        self.model_type = model

    def get_openai_chat_template(
        self,
        user_message: str,
        system_message: Optional[str] = None,
        history: Optional[list] = None,
    ) -> list:
        """Generate an OpenAI chat template with the given user message and optional system message and history."""
        if history is not None:
            messages = history.copy()
        else:
            messages = []

        if system_message is not None:
            if len(messages) > 0 and messages[0]["role"] == "system":
                messages[0]["content"] = system_message
            else:
                messages.insert(0, {"role": "system", "content": system_message})

        messages.append({"role": "user", "content": user_message})

        return messages

    async def query(
        self,
        user_message: str,
        history: Optional[list] = None,
        system_message: Optional[str] = None,
        **kwargs,
    ):
        r"""Asynchronously generates a chat completion using the OpenAI API."""

        system_message = system_message or CHAT_PROMPT_EN
        messages = self.get_openai_chat_template(
            user_message=user_message,
            system_message=system_message,
            history=history,
        )

        response = await self.client.chat.completions.create(
            messages=messages,
            model=self.model_type.value
            if isinstance(self.model_type, OpenAIModelType)
            else self.model_type,
            **kwargs,
        )

        return response
