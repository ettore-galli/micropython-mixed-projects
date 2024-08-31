import asyncio
import sys

from base import BasePin, BaseTime  # type: ignore[import-untyped]


class HardwareInformation:
    def __init__(self) -> None:
        self.led_pin: int = 13
        self.button_pin: int = 4


class OneSecondGameConfiguration:
    def __init__(self) -> None:
        self.reference: int = 1000
        self.delta: int = 400
        self.sequence_initial_delay: float = 0.5
        self.win_sequence: list[tuple[int, float]] = [
            (OneSecondGameEngine.LED_ON, 0.1),
            (OneSecondGameEngine.LED_OFF, 0.1),
            (OneSecondGameEngine.LED_ON, 0.1),
            (OneSecondGameEngine.LED_OFF, 0.1),
            (OneSecondGameEngine.LED_ON, 0.1),
            (OneSecondGameEngine.LED_OFF, 0.1),
            (OneSecondGameEngine.LED_ON, 0.1),
            (OneSecondGameEngine.LED_OFF, 0.1),
            (OneSecondGameEngine.LED_ON, 0.1),
            (OneSecondGameEngine.LED_OFF, 0.1),
        ]
        self.lose_lower_sequence: list[tuple[int, float]] = [
            (OneSecondGameEngine.LED_ON, 0.7),
            (OneSecondGameEngine.LED_OFF, 0.1),
            (OneSecondGameEngine.LED_ON, 0.7),
            (OneSecondGameEngine.LED_OFF, 0.1),
            (OneSecondGameEngine.LED_ON, 1.0),
            (OneSecondGameEngine.LED_OFF, 0.1),
        ]
        self.lose_higher_sequence: list[tuple[int, float]] = [
            (OneSecondGameEngine.LED_ON, 0.7),
            (OneSecondGameEngine.LED_OFF, 0.1),
            (OneSecondGameEngine.LED_ON, 0.7),
            (OneSecondGameEngine.LED_OFF, 0.1),
            (OneSecondGameEngine.LED_ON, 0.1),
            (OneSecondGameEngine.LED_OFF, 0.1),
            (OneSecondGameEngine.LED_ON, 0.1),
            (OneSecondGameEngine.LED_OFF, 0.1),
            (OneSecondGameEngine.LED_ON, 0.1),
            (OneSecondGameEngine.LED_OFF, 0.1),
        ]


class ButtonStatus:
    DEBOUNCE_TIME_NS = 20_000_000
    POLL_TIME = 0.05

    def __init__(self) -> None:
        self.value: int = 0
        self.press_start: int = 0
        self.press_stop: int = 0
        self.last_duration: int = 0
        self.last_trig_time: int = 0


class OneSecondGameResult:
    GAME_RESULT_WIN: int = 2
    GAME_RESULT_GUESSED_LOWER: int = 0
    GAME_RESULT_GUESSED_HIGHER: int = 1


class OneSecondGameEngine:
    LED_ON: int = 1
    LED_OFF: int = 0

    def __init__(
        self,
        time: BaseTime,
        pin_class: type[BasePin],
        use_irq: bool,  # noqa: FBT001
        hardware_information: HardwareInformation | None = None,
        one_second_game_information: OneSecondGameConfiguration | None = None,
    ) -> None:
        self.time: BaseTime = time
        self.pin_class: BasePin = pin_class
        self.use_irq: bool = use_irq

        self.button_status: ButtonStatus = ButtonStatus()

        self.hardware_information = (
            hardware_information
            if hardware_information is not None
            else HardwareInformation()
        )

        self.one_second_game_information = (
            one_second_game_information
            if one_second_game_information is not None
            else OneSecondGameConfiguration()
        )

        self.led = self.pin_class(self.hardware_information.led_pin, self.pin_class.OUT)
        self.button = self.pin_class(
            self.hardware_information.button_pin, self.pin_class.IN
        )
        if self.use_irq:
            self.button.irq(
                trigger=self.pin_class.IRQ_FALLING | self.pin_class.IRQ_RISING,
                handler=self.button_change,
            )

    def log(self, message: str) -> None:
        sys.stdout.write(f"{self.time.ticks_ms()}: {message}\n")

    def set_button_value(self, value: int) -> None:
        self.button_status.value = value
        if value == 1:
            self.set_button_on_state()
        if value == 0:
            self.set_button_off_state()

    def is_value_changed(self, value: int) -> bool:
        return value != self.button_status.value

    def set_button_on_state(self) -> None:
        self.button_status.press_start = self.time.ticks_ms()
        self.led.on()

    def set_button_off_state(self) -> None:
        self.button_status.press_stop = self.time.ticks_ms()
        self.led.off()

    def play_sequence(self, sequence: list[tuple[int, float]]) -> None:
        self.time.sleep(self.one_second_game_information.sequence_initial_delay)
        for state, duration in sequence:
            if state == self.LED_ON:
                self.led.on()
            if state == self.LED_OFF:
                self.led.off()
            self.time.sleep(duration)
        self.led.off()

    def notify_win(self) -> None:
        self.play_sequence(self.one_second_game_information.win_sequence)

    def notify_loose_lower(self) -> None:
        self.play_sequence(self.one_second_game_information.lose_lower_sequence)

    def notify_loose_higher(self) -> None:
        self.play_sequence(self.one_second_game_information.lose_higher_sequence)

    def calculate_game_result(
        self, duration: int, game_configuration: OneSecondGameConfiguration
    ) -> int:
        if duration < game_configuration.reference - game_configuration.delta:
            return OneSecondGameResult.GAME_RESULT_GUESSED_LOWER

        if duration > game_configuration.reference + game_configuration.delta:
            return OneSecondGameResult.GAME_RESULT_GUESSED_HIGHER

        return OneSecondGameResult.GAME_RESULT_WIN

    def notify_game_result(self, game_result: int) -> None:
        action_map = {
            OneSecondGameResult.GAME_RESULT_WIN: self.notify_win,
            OneSecondGameResult.GAME_RESULT_GUESSED_LOWER: self.notify_loose_lower,
            OneSecondGameResult.GAME_RESULT_GUESSED_HIGHER: self.notify_loose_higher,
        }
        action_map.get(game_result, lambda: None)()

    def get_last_duration(self) -> int:
        return self.time.ticks_diff(
            self.button_status.press_stop, self.button_status.press_start
        )

    def button_change(self, pin: BasePin) -> None:
        now: int = self.time.time_ns()
        self.log(
            f"{pin.value()} {now} - {self.button_status.last_trig_time} = "
            f"{now - self.button_status.last_trig_time} "
            f"({now - self.button_status.last_trig_time > ButtonStatus.DEBOUNCE_TIME_NS})"
        )
        if now - self.button_status.last_trig_time > ButtonStatus.DEBOUNCE_TIME_NS:

            self.button_status.last_trig_time = now
            self.perform_trig_action(pin.value())

    def perform_trig_action(self, pin_value: int) -> None:
        self.set_button_value(value=pin_value)
        if pin_value == 0:
            self.perform_game_ending()

    def perform_game_ending(self) -> None:
        game_result: int = self.calculate_game_result(
            duration=self.get_last_duration(),
            game_configuration=self.one_second_game_information,
        )
        self.notify_game_result(game_result=game_result)

    async def button_change_poll(self) -> None:
        while True:
            current_value: int = self.button.value()
            if self.is_value_changed(value=current_value):
                self.log(f"{current_value}\n")
                self.perform_trig_action(pin_value=current_value)

            self.time.sleep(ButtonStatus.POLL_TIME)

    async def main(self) -> None:
        if not self.use_irq:
            button_poll = asyncio.create_task(self.button_change_poll())
            await button_poll
