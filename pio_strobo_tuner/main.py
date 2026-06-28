from typing import TYPE_CHECKING

import rp2
from machine import Pin  # pyright: ignore[reportMissingModuleSource]

if TYPE_CHECKING:
    from rp2.asm_pio import set, pins  # pyright: ignore[reportMissingModuleSource]

STROBO_DISPLAY_PINS = [16, 17, 18, 19, 20]
STROBO_PIO_SM_ID = 1
STROBO_PIO_SM_FREQUENCY = 5000


@rp2.asm_pio(
    set_init=(
        rp2.PIO.OUT_LOW,
        rp2.PIO.OUT_LOW,
        rp2.PIO.OUT_LOW,
        rp2.PIO.OUT_LOW,
        rp2.PIO.OUT_LOW,
    )
)
def strobo_sequence_direct():
    set(pins, 0b00001)[1]
    set(pins, 0b00010)[1]
    set(pins, 0b00100)[1]
    set(pins, 0b01000)[1]
    set(pins, 0b10000)[1]


for p in STROBO_DISPLAY_PINS:
    Pin(p, Pin.OUT)

sm1 = rp2.StateMachine(
    STROBO_PIO_SM_ID,
    strobo_sequence_direct,
    freq=STROBO_PIO_SM_FREQUENCY,
    set_base=Pin(STROBO_DISPLAY_PINS[0]),
)
sm1.active(1)
