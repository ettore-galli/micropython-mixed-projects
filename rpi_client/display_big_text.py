import framebuf  # type: ignore[import-not-found]


#
# https://github.com/orgs/micropython/discussions/16382
#
def write_big_text(  # noqa: PLR0913
    display: framebuf.FrameBuffer, text: str, x: int, y: int, scale_x: int, scale_y: int
) -> None:

    character_width: int = 8
    character_height: int = 8
    fill_scale: int = 2

    # temporary buffer for the text

    width = character_width * len(text)
    height = character_height
    temp_buf = bytearray(width * height)
    temp_fb = framebuf.FrameBuffer(temp_buf, width, height, framebuf.MONO_VLSB)

    # write text to the temporary framebuffer
    temp_fb.text(text, 0, 0, 1)

    w = scale_x
    h = scale_y

    hwl = scale_x - scale_x // fill_scale
    hwr = scale_x - hwl
    hhu = scale_y - scale_y // fill_scale
    hhd = scale_y - hhu

    # scale and write to the display
    for i in range(width):
        for j in range(height):

            pixel = temp_fb.pixel(i, j)

            xr = x + i * scale_x
            yr = y + j * scale_y

            if pixel:  # If the pixel is set, draw a larger rectangle
                display.fill_rect(xr, yr, w, h, 1)
            elif i > 0 and j > 0:

                up = temp_fb.pixel(i, j - 1)
                down = temp_fb.pixel(i, j + 1) if j + 1 < height else 0
                left = temp_fb.pixel(i - 1, j)
                right = temp_fb.pixel(i + 1, j) if i + 1 < width else 0

                if up and left:
                    display.fill_rect(xr, yr, hwr, hhd, 1)
                if up and right:
                    display.fill_rect(xr + hwl, yr, hwl, hhd, 1)
                if down and left:
                    display.fill_rect(xr, yr + hhu, hwr, hhu, 1)
                if down and right:
                    display.fill_rect(xr + hwl, yr + hhu, hwl, hhu, 1)
