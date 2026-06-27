from typing import TYPE_CHECKING

import rp2
from machine import Pin  # pyright: ignore[reportMissingModuleSource]
import time

if TYPE_CHECKING:
    from rp2.asm_pio import (  # pyright: ignore[reportMissingModuleSource]
        set,
        label,
        nop,
        jmp,
        pins,
        x,
        x_dec,
    )



@rp2.asm_pio(
    set_init=(
        rp2.PIO.OUT_LOW,
        rp2.PIO.OUT_LOW,
        rp2.PIO.OUT_LOW,
        rp2.PIO.OUT_LOW,
        rp2.PIO.OUT_LOW,
    )
)
def strobo_sequence():
    set(pins, 0b00001)[31]
    set(x, 31)
    label("loop1")
    nop()[31]
    jmp(x_dec, "loop1")
    # ------------------------------
    set(pins, 0b00010)[31]
    set(x, 31)
    label("loop2")
    nop()[31]
    jmp(x_dec, "loop2")
    # ------------------------------
    set(pins, 0b00100)[31]
    set(x, 31)
    label("loop3")
    nop()[31]
    jmp(x_dec, "loop3")
    # ------------------------------
    set(pins, 0b01000)[31]
    set(x, 31)
    label("loop4")
    nop()[31]
    jmp(x_dec, "loop4")
    # ------------------------------
    set(pins, 0b10000)[31]
    set(x, 31)
    label("loop5")
    nop()[31]
    jmp(x_dec, "loop5")


for p in [16, 17, 18, 19, 20]:
    Pin(p, Pin.OUT)

sm1 = rp2.StateMachine(1, strobo_sequence, freq=3000, set_base=Pin(16))
sm1.active(1)
