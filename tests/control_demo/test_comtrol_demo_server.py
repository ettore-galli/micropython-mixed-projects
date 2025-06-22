from control_demo.control_demo_server import merge_dictionaries


def test_merge_dictionaries() -> None:
    assert merge_dictionaries({}, {"number_of_flashes": ["3"]}) == {
        "number_of_flashes": ["3"]
    }
