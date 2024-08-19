from abc import ABC, abstractmethod
from collections.abc import Callable

from base import BaseTime, Incomplete  # type: ignore[import-not-found]


class BasePin(ABC):
    IRQ_RISING: int = 1
    OUT: int = 1
    OPEN_DRAIN: int = 2
    PULL_UP: int = 1
    IRQ_FALLING: int = 2
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
    def irq(self, handler: Callable, trigger: int) -> Callable[..., Incomplete]:
        pass

    @abstractmethod
    def value(self) -> int:
        pass


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
    def __init__(self) -> None:
        self.press_start: int = 0
        self.press_stop: int = 0
        self.last_duration: int = 0


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
        hardware_information: HardwareInformation | None = None,
        one_second_game_information: OneSecondGameConfiguration | None = None,
    ) -> None:
        self.time = time
        self.pin_class = pin_class

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
        self.button.irq(
            trigger=self.pin_class.IRQ_FALLING | self.pin_class.IRQ_RISING,
            handler=self.button_change,
        )

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
        if pin.value() == 1:
            self.set_button_on_state()
        if pin.value() == 0:
            self.set_button_off_state()
            game_result: int = self.calculate_game_result(
                duration=self.get_last_duration(),
                game_configuration=self.one_second_game_information,
            )
            self.notify_game_result(game_result=game_result)

    async def main(self) -> None:
        pass
