import asyncio

from game_engine import OneSecondGameEngine  # type: ignore[import-not-found]
from hardware import HardwareTime  # type: ignore[import-not-found]

if __name__ == "__main__":
    led_game = OneSecondGameEngine(time=HardwareTime())
    asyncio.run(led_game.main())
