import asyncio

from game_engine import OneSecondGameEngine  # type: ignore[import-untyped]
from hardware import HardwarePin, HardwareTime  # type: ignore[import-untyped]

if __name__ == "__main__":
    led_game = OneSecondGameEngine(
        time=HardwareTime(), pin_class=HardwarePin, use_irq=False
    )
    asyncio.run(led_game.main())
