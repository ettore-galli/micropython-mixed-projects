from abc import ABC, abstractmethod
from typing import Any, TypeAlias

Incomplete: TypeAlias = Any

SpecialPins: TypeAlias = str

PICO_W_INTERNAL_LED_PIN: SpecialPins = "LED"


class BaseTime(ABC):
    @abstractmethod
    async def sleep(self, seconds: float) -> None:
        _ = seconds

    @abstractmethod
    def ticks_ms(self) -> int:
        return 0


class BasePin(ABC):
    OUT: int = 1
    IN: int = 0

    def __init__(self, pin_id: int, mode: int) -> None:
        _ = pin_id, mode

    @abstractmethod
    def on(self) -> None:
        pass

    @abstractmethod
    def off(self) -> None:
        pass

    @abstractmethod
    def value(self) -> int:
        pass


class AccessPointInformation:
    def __init__(self, essid: str, password: str) -> None:
        self.essid: str = essid
        self.password: str = password


class BaseAccessPoint(ABC):
    @abstractmethod
    def __init__(self, access_point_information: AccessPointInformation) -> None: ...
    @abstractmethod
    async def startup(self) -> None:
        pass


class BaseWebServer(ABC):
    @abstractmethod
    def __init__(self) -> None: ...
    @abstractmethod
    async def startup(self) -> None:
        pass


class BaseDataService(ABC):

    def __init__(self, data_file: str) -> None:
        self.data_file = data_file

    @abstractmethod
    def get_data(self) -> dict[str, Any]: ...

    @abstractmethod
    def save_data(self, data: dict[str, Any]) -> None: ...
