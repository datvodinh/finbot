import json
from abc import ABC, abstractmethod


class BaseTool(ABC):
    def __init__(self):
        pass

    def text_to_json(self, text: str) -> dict:
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
