from collections.abc import Callable

import utime as time  # type: ignore[import-not-found]
from machine import Pin  # type: ignore[import-not-found]

from base import Incomplete  # type: ignore[import-untyped]


class HardwareTime:
    def sleep(self, seconds: float) -> None:
        time.sleep(seconds)

    def ticks_ms(self) -> int:
        return time.ticks_ms()

    def time_ns(self) -> int:
        return time.time_ns()

    def ticks_diff(self, ticks1: int, ticks2: int) -> int:
        return time.ticks_diff(ticks1, ticks2)


class HardwarePin:
    IRQ_RISING: int = 1
    OUT: int = 1
    OPEN_DRAIN: int = 2
    PULL_UP: int = 1
    IRQ_FALLING: int = 2
    IN: int = 0

    def __init__(self, pin_id: int, mode: int) -> None:
        self._pin: Pin = Pin(pin_id, mode)

    def on(self) -> None:
        self._pin.on()

    def off(self) -> None:
        self._pin.off()

    def irq(self, handler: Callable, trigger: int) -> Callable[..., Incomplete]:
        return self._pin.irq(handler=handler, trigger=trigger)

    def value(self) -> int:
        return self._pin.value()
