import utime as time  # type: ignore[import-not-found]
from machine import Pin  # type: ignore[import-not-found]


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
    OUT: int = 1
    IN: int = 0

    def __init__(self, pin_id: int, mode: int) -> None:
        self._pin: Pin = Pin(pin_id, mode)

    def on(self) -> None:
        self._pin.on()

    def off(self) -> None:
        self._pin.off()

    def value(self) -> int:
        return self._pin.value()
