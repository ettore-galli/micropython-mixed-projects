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


def generate_pio_strobo_sequence(
    set_void: int = 6, nop_void: int = 29, loop_delay: int = 31
):

    def strobo_sequence():
        set(pins, 0b00001)[set_void]  # Durata: 1 + set_void
        set(x, loop_delay)  # Durata: 1
        label("loop1")  # Durata: loop_delay * (nop_void + 1 + 1)
        nop()[nop_void]  # Durata (di cui): ->  nop_void + 1  per ciclo loop
        jmp(x_dec, "loop1")  # Durata (di cui): -> 1  per ciclo loop
        # ------------------------------
        set(pins, 0b00010)[set_void]  # Durata: simile a loop 1
        set(x, loop_delay)
        label("loop2")
        nop()[nop_void]
        jmp(x_dec, "loop2")
        # ------------------------------
        set(pins, 0b00100)[set_void]  # Durata: simile a loop 1
        set(x, loop_delay)
        label("loop3")
        nop()[nop_void]
        jmp(x_dec, "loop3")
        # ------------------------------
        set(pins, 0b01000)[set_void]  # Durata: simile a loop 1
        set(x, loop_delay)
        label("loop4")
        nop()[nop_void]
        jmp(x_dec, "loop4")
        # ------------------------------
        set(pins, 0b10000)[set_void]  # Durata: simile a loop 1
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
    generate_pio_strobo_sequence(),
    freq=3000,
    set_base=Pin(16),
)
sm1.active(1)
