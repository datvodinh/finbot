import json
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class BaseTool(ABC):
    def __init__(self):
        pass

    def prepare_history(self, history: Optional[List[Dict[str, Any]]]) -> str:
        """Prepare the history for the model input."""
        if not history:
            return ""

        return "\n".join(
            [f"- {message['role']}: {message['content']}" for message in history]
        )

    def text_to_json(self, text: str) -> dict:
        """Convert text to json"""
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            if "```json" in text:
                return json.loads(text.split("```json")[1].replace("```", ""))
        except Exception as e:
            raise e

    @abstractmethod
    async def run(self):
        pass
