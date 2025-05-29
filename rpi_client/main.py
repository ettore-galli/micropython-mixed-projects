import json
import time

import network  # type: ignore[import-not-found]
import urequests  # type: ignore[import-not-found]

from rpi_client.display import Display

CONFIG_FILE_NAME = "config.json"
HTTP_STATUS_OK = 200


class WifiCredentials:
    def __init__(self, ssid: str, password: str) -> None:
        self.ssid: str = ssid
        self.password: str = password


class ConfigReader:
    def __init__(self, config_file: str) -> None:
        self.config_file: str = config_file

    def read_config(self) -> WifiCredentials | None:
        try:
            with open(self.config_file) as f:
                config = json.load(f)
            return WifiCredentials(config["ssid"], config["password"])
        except (OSError, json.JSONDecodeError) as e:
            print("Errore nel caricamento del file JSON:", e)
            return None


def provide_connection(
    credentials: WifiCredentials | None,
    poll_interval: int = 1,
    connection_timeout: int = 10,
) -> network.WLAN | None:
    if credentials is None:
        print("Nessuna credenziale Wi-Fi fornita.")
        return None

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)  # noqa: FBT003  no keyword argument allowed
    wlan.connect(credentials.ssid, credentials.password)
    timeout = connection_timeout
    while not wlan.isconnected() and timeout > 0:
        time.sleep(poll_interval)
        timeout -= 1

    if not wlan.isconnected():
        print("Connessione Wi-Fi fallita!")
        return None

    print("Connesso! IP:", wlan.ifconfig()[0])
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

    def display_result(self, result: str) -> None:
        self.display.clear()
        self.display.text(result, 10, 10, 1)
        self.display.show()

    def read_credentials(self) -> None:
        config_reader = ConfigReader(CONFIG_FILE_NAME)
        self.credentials: WifiCredentials | None = config_reader.read_config()

    def provide_connection(self) -> None:
        self.wlan = provide_connection(
            credentials=self.credentials,
        )

    def make_request(self) -> None:
        if self.wlan is None:
            print("Connessione Wi-Fi non disponibile.")
            return

        try:
            print("Inizio richiesta HTTP...")
            response = urequests.get(self.url)  # GET request

            if response.status_code == HTTP_STATUS_OK:
                print("Risposta dall'API:")
                print(response.json())  # Stampa il JSON ricevuto
                self.display_result(
                    str(response.json().get("title", "Nessun titolo trovato"))
                )

            else:
                print("Errore HTTP:", response.status_code)

        except Exception as e:  # noqa: BLE001
            print("Errore nella richiesta HTTP:", e)

        finally:
            if "response" in locals():
                response.close()  # Chiudi la connessione (importante!)

    def perform(self) -> None:
        while True:
            self.make_request()
            time.sleep(10)


def main() -> None:
    crm = ContinuousRequestMaker(
        url="https://jsonplaceholder.typicode.com/todos/1",  # API di esempio
    )
    crm.read_credentials()
    crm.provide_connection()
    crm.perform()


if __name__ == "__main__":
    main()
