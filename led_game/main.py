import asyncio

from led_ui import LedUI  # type: ignore[import-not-found]

if __name__ == "__main__":
    led_game = LedUI()
    asyncio.run(led_game.main())
