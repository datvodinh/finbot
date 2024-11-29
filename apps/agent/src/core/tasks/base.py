from abc import ABC, abstractmethod


class BaseTask(ABC):
    def __init__(self):
        pass

    @abstractmethod
    async def run(self):
        pass
