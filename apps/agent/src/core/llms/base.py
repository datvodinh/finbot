from abc import ABC, abstractmethod
from typing import List


class BaseModel(ABC):
    pass

    @abstractmethod
    def query(self, message: List[str]) -> str:
        pass
