import gc
import time
from collections.abc import Callable

import network  # type: ignore[import-not-found]
import urequests  # type: ignore[import-not-found]

from rpi_client.base import WifiCredentials
from rpi_client.config_reader import ConfigReader
from rpi_client.display import Display

CONFIG_FILE_NAME = "config.json"
HTTP_STATUS_OK = 200


def provide_connection(
    credentials: WifiCredentials | None,
    printer: Callable,
    poll_interval: int = 1,
    connection_timeout: int = 10,
) -> network.WLAN | None:
    if credentials is None:
        printer("Nessuna credenziale Wi-Fi fornita.")
        return None

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)  # noqa: FBT003  no keyword argument allowed
    wlan.connect(credentials.ssid, credentials.password)
    timeout = connection_timeout
    while not wlan.isconnected() and timeout > 0:
        time.sleep(poll_interval)
        timeout -= 1

    if not wlan.isconnected():
        printer("Connessione Wi-Fi fallita!")
        return None

    printer(f"Connesso! IP: {wlan.ifconfig()[0]}")
    return wlan


class ContinuousRequestMaker:
    def __init__(self, url: str) -> None:
        self.url: str = url
        self.config_file: str
        self.wlan = None
        self.display = Display(
            sda_pin=4,
            scl_pin=5,
        )
        self.intra_request_delay_seconds: float = 10

    def display_text(self, result: str) -> None:
        parts = result.split("T")
        self.display.clear()
        if parts:
            for index, part in enumerate(parts):
                self.display.text(part, 10, 5 + index * 15, 1)
        else:
            self.display.text("<no data>", 10, 10, 1)
        self.display.show()

    def read_credentials(self) -> None:
        config_reader = ConfigReader(CONFIG_FILE_NAME)
        self.credentials: WifiCredentials | None = config_reader.read_config()

    def provide_connection(self) -> None:
        self.wlan = provide_connection(
            credentials=self.credentials,
            printer=self.display_text,
        )

    def make_request(self) -> None:
        if self.wlan is None:
            self.display_text("Connessione Wi-Fi non disponibile.")
            return

        try:
            self.display_text("Inizio richiesta HTTP...")
            response = urequests.get(self.url)  # GET request

            if response.status_code == HTTP_STATUS_OK:
                self.display_text(
                    str(response.json().get("dateTime", "N/A")),
                )

            else:
                self.display_text("Errore HTTP:", response.status_code)

        except Exception as e:  # noqa: BLE001
            self.display_text("Errore nella richiesta HTTP:", e)

        finally:
            if "response" in locals():
                response.close()
            gc.collect()

    def perform(self) -> None:
        while True:
            self.make_request()
            time.sleep(self.intra_request_delay_seconds)


def main() -> None:
    crm = ContinuousRequestMaker(
        url="https://www.timeapi.io/api/Time/current/zone?timeZone=Europe/Rome"
    )
    crm.read_credentials()
    crm.provide_connection()
    crm.perform()


if __name__ == "__main__":
    main()
