import asyncio

import utime as time  # type: ignore[import-not-found]
from machine import Pin  # type: ignore[import-not-found]


class HardwareInformation:
    led_pin: int = 13
    button_pin: int = 4


class ParameterConfiguration:
    pass


class ButtonStatus:
    def __init__(self) -> None:
        self.press_start: int = 0
        self.press_stop: int = 0
        self.last_duration: int = 0

    def get_last_duration(self) -> int:
        return time.ticks_diff(self.press_stop, self.press_start)


class LedUI:
    def __init__(
        self,
        hardware_information: HardwareInformation | None = None,
        parameter_configuration: ParameterConfiguration | None = None,
    ) -> None:

        self.button_status: ButtonStatus = ButtonStatus()

        self.hardware_information = (
            hardware_information
            if hardware_information is not None
            else HardwareInformation()
        )

        self.parameter_configuration = (
            parameter_configuration
            if parameter_configuration is not None
            else ParameterConfiguration()
        )

        self.led = Pin(self.hardware_information.led_pin, Pin.OUT)
        self.button = Pin(self.hardware_information.button_pin, Pin.IN)
        self.button.irq(
            trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=self.button_change
        )

    async def led_loop(self) -> None:
        while True:
            self.led.on()
            await asyncio.sleep(0.3)
            self.led.off()
            await asyncio.sleep(3)

    def set_button_on_state(self) -> None:
        self.button_status.press_start = time.ticks_ms()

    def set_button_off_state(self) -> None:
        self.button_status.press_stop = time.ticks_ms()

    def button_change(self, pin: Pin) -> None:
        if pin.value() == 1:
            self.set_button_on_state()
        if pin.value() == 0:
            self.set_button_off_state()
            print(self.button_status.get_last_duration())  # noqa: T201

    async def main(self) -> None:
        led = asyncio.create_task(self.led_loop())
        await asyncio.gather(led)


if __name__ == "__main__":
    theremin = LedUI()
    asyncio.run(theremin.main())
