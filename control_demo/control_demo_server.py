import asyncio

from control_demo_base import BaseWebServer  # type: ignore[import-not-found]
from microdot.microdot import Microdot  # type: ignore[import-not-found]


class WebServer(BaseWebServer):
    def __init__(self) -> None:
        self.app = Microdot()

        @self.app.route("/")
        async def index(request) -> str:  # noqa: ANN001 ARG001
            return "Hello, world!"

    async def startup(self) -> None:
        server = asyncio.create_task(self.app.start_server())
        await server
