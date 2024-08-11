import asyncio
from collections.abc import Callable

from machine import ADC, PWM, Pin  # type: ignore[import-not-found]


class HardwareInformation:
    pwm_pins: list[int] = [0, 2, 4, 6, 8, 10, 12, 14]
    pwm_freqs: list[int] = [int(220 * (2 ** (tone / 6))) for tone in range(8)]


class ParameterConfiguration:
    adc_delay: float = 0.01


class PWMOrgan:
    def __init__(
        self,
        hardware_information: HardwareInformation | None = None,
        parameter_configuration: ParameterConfiguration | None = None,
    ) -> None:
        self.hardware_information = (
            hardware_information
            if hardware_information is not None
            else HardwareInformation()
        )

        self.parameter_configuration = (
            parameter_configuration
            if parameter_configuration is not None
            else ParameterConfiguration()
        )

        self.pwm_sources = [
            PWM(Pin(pin), freq=freq, duty_u16=32768)
            for pin, freq in zip(
                self.hardware_information.pwm_pins, self.hardware_information.pwm_freqs
            )
        ]

    async def main(self) -> None:
        pass


if __name__ == "__main__":
    organ = PWMOrgan()
    asyncio.run(organ.main())
