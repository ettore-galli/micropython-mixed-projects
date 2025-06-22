import json
from collections.abc import Callable
from typing import Any

from control_demo_base import BaseDataService  # type: ignore[import-not-found]


class DataService(BaseDataService):
    def __init__(self, data_file: str, logger: Callable[[str], None]) -> None:
        super().__init__(data_file)
        self.logger: Callable[[str], None] = logger

    def get_data(self) -> dict[str, Any]:
        try:
            with open(self.data_file, encoding="utf-8") as datafile:
                return json.load(datafile)
        except OSError as error:
            self.logger(str(error))
            return {}

    def save_data(self, data: dict[str, Any]) -> None:
        try:
            with open(self.data_file, "w", encoding="utf-8") as datafile:
                return json.dump(data, datafile)
        except OSError as error:
            self.logger(str(error))
