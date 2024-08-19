import utime as time  # type: ignore[import-not-found]


class HardwareTime:
    def sleep(self, seconds: float) -> None:
        time.sleep(seconds)

    def ticks_ms(self) -> int:
        return time.ticks_ms()

    def ticks_diff(self, ticks1: int, ticks2: int) -> int:
        return time.ticks_diff(ticks1, ticks2)
