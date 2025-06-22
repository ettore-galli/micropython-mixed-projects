from unittest.mock import MagicMock

from control_demo.control_demo_server import (
    get_data_from_request,
    merge_dictionaries,
    render_page_using_data,
)
from microdot.microdot import MultiDict  # type: ignore[import-not-found]


def test_merge_dictionaries() -> None:
    assert merge_dictionaries({}, {"number_of_flashes": ["3"]}) == {
        "number_of_flashes": ["3"]
    }


def test_get_data_from_request() -> None:
    request = MagicMock()
    request.form = MultiDict({"number_of_flashes": "3"})

    assert get_data_from_request(request=request) == {"number_of_flashes": "3"}


def test_render_page_using_data() -> None:
    raw_page = '<input type="number" name="number_of_flashes" id="number_of_flashes" value="**NUMBER_OF_FLASHES**">'
    rendering_data = {"number_of_flashes": ["3"]}
    assert (
        render_page_using_data(raw_page=raw_page, raw_data=rendering_data)
        == '<input type="number" name="number_of_flashes" id="number_of_flashes" value="[\'3\']">'
    )
