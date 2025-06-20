import asyncio

from control_demo_base import BaseWebServer  # type: ignore[import-not-found]
from microdot.microdot import Microdot  # type: ignore[import-not-found]

WEB_PAGES_PATH: str = "./web"
WEB_PAGES: dict[str, str] = {"index": "index.html"}

HTTP_OK = 200


def get_page_file_by_id(page_id: str) -> str:
    return f"{WEB_PAGES_PATH}/{WEB_PAGES.get(page_id)}"


def get_page_content(page_id: str) -> tuple[str, int, dict[str, str]]:
    with open(get_page_file_by_id(page_id), encoding="utf-8") as page:
        html_content = page.read()
        return html_content, HTTP_OK, {"Content-Type": "text/html"}


class WebServer(BaseWebServer):
    def __init__(self) -> None:
        self.app = Microdot()

        @self.app.route("/")
        async def index(
            request,  # noqa: ANN001 ARG001
        ) -> tuple[str, int, dict[str, str]]:
            return get_page_content("index")

    async def startup(self) -> None:
        server = asyncio.create_task(self.app.start_server())
        await server
