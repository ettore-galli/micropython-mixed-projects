import asyncio

from machine import Pin  # type: ignore[import-not-found]


class HardwareTime:
    async def sleep(self, seconds: float) -> None:
        await asyncio.sleep(seconds)


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
