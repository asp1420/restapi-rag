
from abc import ABC, abstractmethod
from typing import Any


class Processor(ABC):

    @abstractmethod
    def run(self) -> None: ...

    @abstractmethod
    def get(self) -> Any: ...
