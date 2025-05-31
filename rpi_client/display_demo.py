from rpi_client.display import Display


class DisplayDemo:
    def __init__(self) -> None:
        self.display = Display(
            sda_pin=4,
            scl_pin=5,
        )

    def display_text(self, result: str) -> None:
        parts = result.split("|")
        self.display.clear()
        if parts:
            for index, part in enumerate(parts):
                self.display.text(part, 10, 5 + index * 15, 1)
        else:
            self.display.text("<no data>", 10, 10, 1)
        self.display.show()

    def perform(self) -> None:
        while True:
            self.display.big_text("12:59", 1, 10, scale_x=3, scale_y=6)
            self.display.show()


def main() -> None:
    crm = DisplayDemo()
    crm.perform()


if __name__ == "__main__":
    main()
