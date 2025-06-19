import asyncio

import network  # type: ignore[import-not-found]
import utime as time  # type: ignore[import-not-found]
from control_demo_base import (  # type: ignore[import-not-found]
    AccessPointInformation,
    BaseAccessPoint,
    BasePin,
    BaseTime,
)
from machine import Pin  # type: ignore[import-not-found]


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


ACCESS_POINT_INFORMATION = AccessPointInformation(
    essid="CONFIG-HOST", password="password!"  # noqa: S106
)


class AccessPoint(BaseAccessPoint):
    def __init__(self, access_point_information: AccessPointInformation) -> None:
        super().__init__(access_point_information=access_point_information)
        self.access_point_information = access_point_information

    async def startup(self) -> None:
        ap = network.WLAN(network.AP_IF)
        ap.config(
            essid=self.access_point_information.essid,
            password=self.access_point_information.password,
        )
        ap.active(True)  # noqa: FBT003
