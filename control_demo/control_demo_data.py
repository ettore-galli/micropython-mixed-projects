import json
from typing import Any

from control_demo.control_demo_base import BaseDataManager


class DataManager(BaseDataManager):

    def get_data(self) -> dict[str, Any]:
        with open(self.data_file, encoding="utf-8") as datafile:
            return json.load(datafile)

    def save_data(self, data: dict[str, Any]) -> None:
        with open(self.data_file, "w", encoding="utf-8") as datafile:
            return json.dump(data, datafile)
