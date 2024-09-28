from abc import ABC, abstractmethod


class BaseADC(ABC):
    @abstractmethod
    def __init__(self, pin: int) -> None: ...

    @abstractmethod
    def read_u16(self) -> int: ...
