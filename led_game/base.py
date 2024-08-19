from abc import ABC, abstractmethod
from typing import Any, TypeAlias

Incomplete: TypeAlias = Any


class BaseTime(ABC):
    @abstractmethod
    def sleep(self, seconds: float) -> None:
        _ = seconds

    @abstractmethod
    def ticks_ms(self) -> int:
        return 0

    @abstractmethod
    def ticks_diff(self, ticks1: int, ticks2: int) -> int:
        _ = ticks1, ticks2
        return 0
