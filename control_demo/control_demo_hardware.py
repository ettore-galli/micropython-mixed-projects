import asyncio
from collections.abc import Callable

import network  # type: ignore[import-not-found]
import utime as time  # type: ignore[import-not-found]
from control_demo_base import (  # type: ignore[import-not-found, import-untyped]
    EMPTY_WIFI_CLIENT_INFORMATION,
    AccessPointInformation,
    BaseAccessPoint,
    BasePin,
    BaseTime,
    BaseWifiClient,
    WifiClientInformation,
    rpi_logger,
)
from control_demo_data import get_wifi_data_service  # type: ignore[import-not-found, import-untyped]
from machine import Pin  # type: ignore[import-not-found, import-untyped]


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
    ssid="CONFIG-HOST", password="password!"  # noqa: S106
)


class AccessPoint(BaseAccessPoint):
    def __init__(self, access_point_information: AccessPointInformation) -> None:
        super().__init__(access_point_information=access_point_information)
        self.access_point_information = access_point_information
        self.logger = rpi_logger

    async def startup(self) -> None:
        ap = network.WLAN(network.AP_IF)
        ap.config(
            ssid=self.access_point_information.ssid,
            password=self.access_point_information.password,
        )
        ap.active(True)  # noqa: FBT003


class WifiClient(BaseWifiClient):
    def __init__(
        self, wifi_client_information_retriever: Callable[[], WifiClientInformation]
    ) -> None:
        super().__init__(
            wifi_client_information_retriever=wifi_client_information_retriever
        )
        self.wifi_client_information_retriever = wifi_client_information_retriever
        self.logger = rpi_logger

        self.wifi_client_information: WifiClientInformation = (
            EMPTY_WIFI_CLIENT_INFORMATION
        )

    async def startup(
        self,
        poll_interval: int = 1,
        connection_timeout: int = 10,
    ) -> None:

        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)  # noqa: FBT003  no keyword argument allowed
        self.wifi_client_information = self.wifi_client_information_retriever()
        wlan.connect(
            self.wifi_client_information.ssid, self.wifi_client_information.password
        )
        timeout = connection_timeout
        while not wlan.isconnected() and timeout > 0:
            time.sleep(poll_interval)
            timeout -= 1

        if not wlan.isconnected():
            self.logger("Wi-Fi connection failed.")
            return

        self.logger(f"Connected! IP: {wlan.ifconfig()[0]}")


def retrieve_wifi_client_information() -> WifiClientInformation:
    data = get_wifi_data_service()
    credentials = data.get_data()
    if credentials:
        return WifiClientInformation(
            ssid=credentials["ssid"], password=credentials["password"]
        )
    return EMPTY_WIFI_CLIENT_INFORMATION
