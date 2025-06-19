from abc import ABC, abstractmethod
from typing import Any, TypeAlias

Incomplete: TypeAlias = Any

SpecialPins: TypeAlias = str

PICO_W_INTERNAL_LED_PIN: SpecialPins = "LED"


class BaseTime(ABC):
    @abstractmethod
    async def sleep(self, seconds: float) -> None:
        _ = seconds

    @abstractmethod
    def ticks_ms(self) -> int:
        return 0


class BasePin(ABC):
    OUT: int = 1
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
    def value(self) -> int:
        pass


class BaseSerialCommunicator(ABC):
    @abstractmethod
    async def serial_loop(self) -> None:
        pass
