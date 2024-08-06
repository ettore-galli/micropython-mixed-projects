import asyncio
from collections.abc import Callable  # * noqa: UP035

from machine import ADC, PWM, Pin  # type: ignore[import-not-found]


class HardwareInformation:
    adc_gpio_pin: int = 26
    speaker_pwm_pin: int = 0
    miminum_pwm_frequency = 20
    maximum_pwm_frequency = 700
    adc_range_top = 20000
    adc_range_bottom = 5000


class ParameterConfiguration:
    adc_delay: float = 0.01


class PWMTheremin:
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

        self.adc = ADC(Pin(self.hardware_information.adc_gpio_pin))

        self.speaker_pwm = PWM(
            Pin(self.hardware_information.speaker_pwm_pin), freq=1000, duty_u16=32768
        )

    async def read_adc_values_loop(
        self,
        sample_value_reader: Callable[[], int],
        sample_value_consumer: Callable[[int], None],
    ) -> None:

        while True:
            raw_adc_value = sample_value_reader()
            sample_value_consumer(raw_adc_value)
            await asyncio.sleep(self.parameter_configuration.adc_delay)

    async def main(self) -> None:
        await self.read_adc_values_loop(
            sample_value_reader=self.adc.read_u16,
            sample_value_consumer=self.set_value,
        )

    def get_frequency_value(self, raw_adc_value: int) -> float:
        return self.hardware_information.miminum_pwm_frequency + (
            self.hardware_information.maximum_pwm_frequency
            * (
                raw_adc_value
                / (
                    self.hardware_information.adc_range_top
                    - self.hardware_information.adc_range_bottom
                )
            )
        )

    def get_frequency_value_nonlinear(self, raw_adc_value: int) -> float:
        if raw_adc_value < self.hardware_information.adc_range_bottom:
            return self.hardware_information.miminum_pwm_frequency

        adc_range = (
            self.hardware_information.adc_range_top
            - self.hardware_information.adc_range_bottom
        )
        relative = (
            (raw_adc_value - self.hardware_information.adc_range_bottom) / adc_range
        ) ** 0.3

        return self.hardware_information.maximum_pwm_frequency * relative

    def set_value(self, raw_adc_value: int) -> None:
        frequency_value = self.get_frequency_value_nonlinear(raw_adc_value)
        if frequency_value > self.hardware_information.miminum_pwm_frequency:
            self.speaker_pwm.freq(int(frequency_value))


if __name__ == "__main__":
    theremin = PWMTheremin()
    asyncio.run(theremin.main())
