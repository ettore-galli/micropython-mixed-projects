from abc import ABC, abstractmethod
from collections.abc import Callable
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


class BasePin(ABC):
    IRQ_RISING: int = 1
    OUT: int = 1
    OPEN_DRAIN: int = 2
    PULL_UP: int = 1
    IRQ_FALLING: int = 2
    IN: int = 0

    def __init__(self, pin_id: int, mode: int) -> None:
        _ = pin_id, mode

    @abstractmethod
    def on(self) -> None:
        pass

    @abstractmethod
    def off(self) -> None:
        pass

    @abstractmethod
    def irq(self, handler: Callable, trigger: int) -> Callable[..., Incomplete]:
        pass

    @abstractmethod
    def value(self) -> int:
        pass
