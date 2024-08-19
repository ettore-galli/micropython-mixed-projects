import asyncio

from game_engine import OneSecondGameEngine  # type: ignore[import-not-found]

if __name__ == "__main__":
    led_game = OneSecondGameEngine()
    asyncio.run(led_game.main())
