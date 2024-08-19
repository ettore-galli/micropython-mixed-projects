from unittest.mock import MagicMock

from led_game.game_engine import (
    OneSecondGameConfiguration,
    OneSecondGameEngine,
    OneSecondGameResult,
)


def test_calculate_game_result() -> None:
    led_game = OneSecondGameEngine(time=MagicMock(), pin_class=MagicMock())
    result = led_game.calculate_game_result(
        duration=700, game_configuration=OneSecondGameConfiguration()
    )
    assert result == OneSecondGameResult.GAME_RESULT_WIN
