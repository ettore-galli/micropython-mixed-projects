import asyncio
from typing import Any

from control_demo_base import BaseDataService, BaseWebServer  # type: ignore[import-not-found, import-untyped]
from control_demo_data import DataService  # type: ignore[import-not-found, import-untyped]
from microdot.microdot import Microdot, Request  # type: ignore[import-not-found, import-untyped]

WEB_PAGES_PATH: str = "./web"


WEB_PAGE_INDEX_WIFI = "wifi"
WEB_PAGE_INDEX_LED = "led"

WEB_PAGES: dict[str, str] = {
    WEB_PAGE_INDEX_LED: "led.html",
    WEB_PAGE_INDEX_WIFI: "wifi.html",
}


HTTP_OK = 200

METHOD_GET: str = "GET"
METHOD_POST: str = "POST"


def get_page_file_by_id(page_id: str) -> str:
    return f"{WEB_PAGES_PATH}/{WEB_PAGES.get(page_id)}"


def get_raw_page_content(page_id: str) -> str:
    with open(get_page_file_by_id(page_id), encoding="utf-8") as page:
        return page.read()


def get_page_content(page_id: str) -> tuple[str, int, dict[str, str]]:
    with open(get_page_file_by_id(page_id), encoding="utf-8") as page:
        html_content = page.read()
        return html_content, HTTP_OK, {"Content-Type": "text/html"}


def build_page_response(rendered_html_content: str) -> tuple[str, int, dict[str, str]]:
    return rendered_html_content, HTTP_OK, {"Content-Type": "text/html"}


def get_data_from_request(request: Request) -> dict[str, Any]:
    return {key: request.form.get(key, None) for key in request.form}


def render_page_using_data(raw_page: str, raw_data: dict) -> str:
    def field_template_tag(field: str) -> str:
        return f"**{field.upper()}**"

    rendered = raw_page
    for field, value in raw_data.items():
        rendered = rendered.replace(field_template_tag(field), str(value))
    return rendered


def merge_dictionaries(
    dict_alfa: dict[Any, Any], dict_beta: dict[Any, Any]
) -> dict[Any, Any]:
    merged: dict[Any, Any] = {}
    for dictionary in [dict_alfa, dict_beta]:
        merged.update(dictionary)

    return merged


async def process_page_repl(
    data_service: BaseDataService,
    page_id: str,
    invariant_rendering_data: dict[str, Any],
    request: Request,
) -> tuple[str, int, dict[str, str]]:
    raw_page_content: str = get_raw_page_content(page_id=page_id)

    if request.method == METHOD_POST:
        request_data: dict[str, Any] = get_data_from_request(request=request)
        rendering_data = merge_dictionaries(invariant_rendering_data, request_data)
        data_service.save_data(data=request_data)

    saved_data = data_service.get_data()
    rendering_data = merge_dictionaries(invariant_rendering_data, saved_data)
    rendered_page = render_page_using_data(
        raw_page=raw_page_content,
        raw_data=rendering_data,
    )

    return build_page_response(rendered_html_content=rendered_page)


class WebServer(BaseWebServer):

    def __init__(self) -> None:
        self.app = Microdot()
        self.led_data_service = DataService(data_file="./data/led.json", logger=print)
        self.wifi_data_service = DataService(data_file="./data/wifi.json", logger=print)

        @self.app.route("/led", methods=[METHOD_GET, METHOD_POST])
        async def led_page(
            request: Request,
        ) -> tuple[str, int, dict[str, str]]:
            return await process_page_repl(
                data_service=self.led_data_service,
                page_id=WEB_PAGE_INDEX_LED,
                invariant_rendering_data={"action": WEB_PAGE_INDEX_LED},
                request=request,
            )

        @self.app.route("/wifi", methods=[METHOD_GET, METHOD_POST])
        async def wifi_page(
            request: Request,
        ) -> tuple[str, int, dict[str, str]]:
            return await process_page_repl(
                data_service=self.wifi_data_service,
                page_id=WEB_PAGE_INDEX_WIFI,
                invariant_rendering_data={"action": WEB_PAGE_INDEX_WIFI},
                request=request,
            )

    async def startup(self) -> None:
        server = asyncio.create_task(self.app.start_server())
        await server
