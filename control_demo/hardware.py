import asyncio

import utime as time  # type: ignore[import-not-found]
from control_demo_base import BasePin, BaseSerialCommunicator, BaseTime  # type: ignore[import-not-found]
from machine import UART, Pin  # type: ignore[import-not-found]


class HardwareTime(BaseTime):
    async def sleep(self, seconds: float) -> None:
        await asyncio.sleep(seconds)

    def ticks_ms(self) -> int:
        return time.ticks_ms()


class HardwarePin(BasePin):
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


class SerialCommunicator(BaseSerialCommunicator):
    def __init__(self) -> None:
        super().__init__()
        self.uart = UART(0, baudrate=115200)

    async def serial_loop(self) -> None:
        while True:
            if self.uart.any():
                try:
                    line = self.uart.readline()
                    if line:
                        command = line.decode("utf-8").strip()
                        print("Received:", command)

                except Exception as e:  # noqa: BLE001
                    print("Error:", e)
            await asyncio.sleep_ms(10)
