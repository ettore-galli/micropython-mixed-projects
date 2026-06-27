from typing import TYPE_CHECKING

import rp2
from machine import Pin  # pyright: ignore[reportMissingModuleSource]

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


def generate_pio_strobo_sequence(set_void: int, nop_void: int, loop_delay: int):

    def strobo_sequence():
        set(pins, 0b00001)[set_void]  # 1 + delay
        set(x, loop_delay)  # 1
        label("loop1")  # 32(delay + 1 + 1)
        nop()[nop_void]  # di cui delay + 1  per ciclo
        jmp(x_dec, "loop1")  # di cui 1  per ciclo
        # ------------------------------
        set(pins, 0b00010)[set_void]
        set(x, loop_delay)
        label("loop2")
        nop()[nop_void]
        jmp(x_dec, "loop2")
        # ------------------------------
        set(pins, 0b00100)[set_void]
        set(x, loop_delay)
        label("loop3")
        nop()[nop_void]
        jmp(x_dec, "loop3")
        # ------------------------------
        set(pins, 0b01000)[set_void]
        set(x, loop_delay)
        label("loop4")
        nop()[nop_void]
        jmp(x_dec, "loop4")
        # ------------------------------
        set(pins, 0b10000)[set_void]
        set(x, loop_delay)
        label("loop5")
        nop()[nop_void]
        jmp(x_dec, "loop5")

    decorated = rp2.asm_pio(
        set_init=(
            rp2.PIO.OUT_LOW,
            rp2.PIO.OUT_LOW,
            rp2.PIO.OUT_LOW,
            rp2.PIO.OUT_LOW,
            rp2.PIO.OUT_LOW,
        )
    )(strobo_sequence)

    return decorated


for p in [16, 17, 18, 19, 20]:
    Pin(p, Pin.OUT)

sm1 = rp2.StateMachine(
    1,
    generate_pio_strobo_sequence(set_void=0, nop_void=9, loop_delay=30),
    freq=3000,
    set_base=Pin(16),
)
sm1.active(1)
