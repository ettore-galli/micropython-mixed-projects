import asyncio

from game_engine import OneSecondGameEngine  # type: ignore[import-not-found]
from hardware import HardwarePin, HardwareTime  # type: ignore[import-not-found]

if __name__ == "__main__":
    led_game = OneSecondGameEngine(time=HardwareTime(), pin_class=HardwarePin)
    asyncio.run(led_game.main())
