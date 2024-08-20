from typing import TYPE_CHECKING
from unittest.mock import MagicMock, call, patch

import pytest
from led_game.game_engine import (
    OneSecondGameConfiguration,
    OneSecondGameEngine,
    OneSecondGameResult,
)

if TYPE_CHECKING:
    from collections.abc import Callable


def test_set_button_on_state() -> None:
    mock_pin_class = MagicMock()
    led_game = OneSecondGameEngine(time=MagicMock(), pin_class=mock_pin_class)
    led_game.set_button_on_state()
    calls = list(mock_pin_class.mock_calls)
    calls[-1] = call().on()


def test_set_button_off_state() -> None:
    mock_pin_class = MagicMock()
    led_game = OneSecondGameEngine(time=MagicMock(), pin_class=mock_pin_class)
    led_game.set_button_off_state()
    calls = list(mock_pin_class.mock_calls)
    calls[-1] = call().off()


def test_play_sequence() -> None:
    mock_time = MagicMock()
    mock_pin_class = MagicMock()
    led_game = OneSecondGameEngine(time=mock_time, pin_class=mock_pin_class)
    led_game.play_sequence([(1, 0.1), (0, 0.2), (1, 0.3)])
    pin_calls = list(mock_pin_class.mock_calls)
    assert [call for call in pin_calls if call in (call().on(), call().off())] == [
        call for call in pin_calls if call in (call().on(), call().off())
    ]
    sleep_calls = list(mock_time.sleep.mock_calls)
    assert [call.args for call in sleep_calls] == [(0.5,), (0.1,), (0.2,), (0.3,)]


@pytest.mark.parametrize(
    ("method_name", "expected_sequence"),
    [
        pytest.param(
            "notify_win",
            [
                (1, 0.1),
                (0, 0.1),
                (1, 0.1),
                (0, 0.1),
                (1, 0.1),
                (0, 0.1),
                (1, 0.1),
                (0, 0.1),
                (1, 0.1),
                (0, 0.1),
            ],
            id="win",
        ),
        pytest.param(
            "notify_loose_lower",
            [
                (1, 0.7),
                (0, 0.1),
                (1, 0.7),
                (0, 0.1),
                (1, 1.0),
                (0, 0.1),
            ],
            id="loose lower",
        ),
        pytest.param(
            "notify_loose_higher",
            [
                (1, 0.7),
                (0, 0.1),
                (1, 0.7),
                (0, 0.1),
                (1, 0.1),
                (0, 0.1),
                (1, 0.1),
                (0, 0.1),
                (1, 0.1),
                (0, 0.1),
            ],
            id="loose higher",
        ),
    ],
)
@patch("led_game.game_engine.OneSecondGameEngine.play_sequence")
def test_notify(
    mock_play_sequence: MagicMock,
    method_name: str,
    expected_sequence: list[tuple[int, float]],
) -> None:
    mock_time = MagicMock()
    mock_pin_class = MagicMock()
    led_game = OneSecondGameEngine(
        time=mock_time,
        pin_class=mock_pin_class,
    )

    notify_method: Callable[[], None] = getattr(led_game, method_name, lambda: None)

    notify_method()

    notify_calls = list(mock_play_sequence.mock_calls)
    assert notify_calls[0].args == (expected_sequence,)


def test_calculate_game_result() -> None:
    led_game = OneSecondGameEngine(time=MagicMock(), pin_class=MagicMock())
    result = led_game.calculate_game_result(
        duration=700, game_configuration=OneSecondGameConfiguration()
    )
    assert result == OneSecondGameResult.GAME_RESULT_WIN


def test_get_last_duration() -> None:
    mock_time = MagicMock()
    mock_pin_class = MagicMock()
    led_game = OneSecondGameEngine(
        time=mock_time,
        pin_class=mock_pin_class,
    )
    led_game.button_status.press_start = 123
    led_game.button_status.press_stop = 369

    led_game.get_last_duration()

    assert next(iter(mock_time.ticks_diff.mock_calls)).args == (369, 123)
