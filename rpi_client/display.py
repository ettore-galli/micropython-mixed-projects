import framebuf  # type: ignore[import-not-found]
from machine import I2C, Pin  # type: ignore[import-not-found]

from rpi_client.base import BaseDisplay
from rpi_client.ssd1306 import SSD1306_I2C  # type: ignore[attr-defined]


class Display(BaseDisplay):
    def __init__(self, sda_pin: int, scl_pin: int) -> None:
        i2c = I2C(sda=Pin(sda_pin), scl=Pin(scl_pin))
        self.display: SSD1306_I2C = SSD1306_I2C(128, 64, i2c)

    def clear(self) -> None:
        self.display.fill(0)

    def text(self, text: str, x: int, y: int, color: int) -> None:
        self.display.text(text, x, y, color)

    def show(self) -> None:
        self.display.show()

    def show_value(self, value: int) -> None:
        self.clear()
        self.text(f"v: {value}", 10, 1, 1)
        self.show()

    def plot_dft(self, values: list[int]) -> None:
        self.clear()
        span = 64 // len(values)
        for index, value in enumerate(values):
            y_coord = span * index
            self.hline(1, y_coord, value, 1)
        self.show()

    def hline(self, x: int, y: int, width: int, color: int) -> None:
        self.display.hline(x, y, width, color)

    def big_text(  # noqa: PLR0913
        self,
        text: str,
        x: int,
        y: int,
        character_width: int = 8,
        character_height: int = 8,
        scale_x: int = 2,
        scale_y: int = 2,
    ) -> None:
        # temporary buffer for the text

        width = character_width * len(text)
        height = character_height
        temp_buf = bytearray(width * height)
        temp_fb = framebuf.FrameBuffer(temp_buf, width, height, framebuf.MONO_VLSB)

        # write text to the temporary framebuffer
        temp_fb.text(text, 0, 0, 1)

        w = scale_x
        h = scale_y

        hw = scale_x - scale_x // 2
        hh = scale_y - scale_y // 2

        # scale and write to the display
        for i in range(width):
            for j in range(height):

                pixel = temp_fb.pixel(i, j)

                xr = x + i * scale_x
                yr = y + j * scale_y

                if pixel:  # If the pixel is set, draw a larger rectangle
                    self.display.fill_rect(xr, yr, w, h, 1)
                elif i > 0 and j > 0:

                    up = temp_fb.pixel(i, j - 1)
                    down = temp_fb.pixel(i, j + 1) if j + 1 < height else 0
                    left = temp_fb.pixel(i - 1, j)
                    right = temp_fb.pixel(i + 1, j) if i + 1 < width else 0

                    if up and left:
                        self.display.fill_rect(xr, yr, hw, hh, 1)
                    if up and right:
                        self.display.fill_rect(xr + hw, yr, hw, hh, 1)
                    if down and left:
                        self.display.fill_rect(xr, yr + hh, hw, hh, 1)
                    if down and right:
                        self.display.fill_rect(xr + hw, yr + hh, hw, hh, 1)
