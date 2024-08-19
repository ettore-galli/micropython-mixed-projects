import utime as time  # type: ignore[import-not-found]
from machine import Pin  # type: ignore[import-not-found]


class HardwareInformation:
    def __init__(self) -> None:
        self.led_pin: int = 13
        self.button_pin: int = 4


class ParameterConfiguration:
    def __init__(self) -> None:
        pass


class OneSecondGameConfiguration:
    def __init__(self) -> None:
        self.reference = 1000
        self.delta = 400


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
        one_second_game_information: OneSecondGameConfiguration | None = None,
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

        self.one_second_game_information = (
            one_second_game_information
            if one_second_game_information is not None
            else OneSecondGameConfiguration()
        )

        self.led = Pin(self.hardware_information.led_pin, Pin.OUT)
        self.button = Pin(self.hardware_information.button_pin, Pin.IN)
        self.button.irq(
            trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=self.button_change
        )

    def set_button_on_state(self) -> None:
        self.button_status.press_start = time.ticks_ms()
        self.led.on()

    def set_button_off_state(self) -> None:
        self.button_status.press_stop = time.ticks_ms()
        self.led.off()

    def notify_win(self) -> None:
        time.sleep(0.5)
        for _ in range(10):
            self.led.on()
            time.sleep(0.1)
            self.led.off()
            time.sleep(0.1)

    def notify_loose(self) -> None:
        time.sleep(0.5)
        for _ in range(3):
            self.led.on()
            time.sleep(0.7)
            self.led.off()
            time.sleep(0.7)

    def button_change(self, pin: Pin) -> None:
        if pin.value() == 1:
            self.set_button_on_state()
        if pin.value() == 0:
            self.set_button_off_state()
            if (
                abs(
                    self.button_status.get_last_duration()
                    - self.one_second_game_information.reference
                )
                < self.one_second_game_information.delta
            ):
                self.notify_win()
            else:
                self.notify_loose()

    async def main(self) -> None:
        pass
