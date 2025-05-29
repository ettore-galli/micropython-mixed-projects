import json

from rpi_client.base import BaseConfigReader, WifiCredentials


class ConfigReader(BaseConfigReader):
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
