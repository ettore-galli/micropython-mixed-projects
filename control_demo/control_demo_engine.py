import asyncio
import sys
from typing import TYPE_CHECKING

from control_demo_base import PICO_W_INTERNAL_LED_PIN, BasePin, BaseTime  # type: ignore[import-not-found]

if TYPE_CHECKING:
    from control_demo_base import SpecialPins


class HardwareInformation:
    def __init__(self) -> None:
        self.led_pin: int | SpecialPins = PICO_W_INTERNAL_LED_PIN


class ControlDemoEngine:
    LED_ON: int = 1
    LED_OFF: int = 0

    def __init__(
        self,
        time: BaseTime,
        pin_class: type[BasePin],
        hardware_information: HardwareInformation | None = None,
    ) -> None:
        self.time: BaseTime = time
        self.pin_class: BasePin = pin_class

        self.hardware_information = (
            hardware_information
            if hardware_information is not None
            else HardwareInformation()
        )

        self.led = self.pin_class(self.hardware_information.led_pin, self.pin_class.OUT)

    def log(self, message: str) -> None:
        sys.stdout.write(f"{self.time.ticks_ms()}: {message}\n")

    async def led_loop(self) -> None:
        while True:
            print("hola", self.hardware_information.led_pin)
            self.led.on()
            self.log("on")
            self.time.sleep(1)

            self.led.off()
            self.log("off")
            self.time.sleep(1)

    async def main(self) -> None:
        await asyncio.gather(self.led_loop())
