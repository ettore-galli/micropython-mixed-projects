import asyncio
from typing import Optional

from machine import ADC, PWM, Pin  # type: ignore[import-not-found]


class HardwareInformation:
    adc_gpio_pin: int = 26
    speaker_pwm_pin: int = 0
    miminum_pwm_frequency = 20
    maximum_pwm_frequency = 1300
    adc_range_top = 25000
    adc_range_bottom = 3000


class ParameterConfiguration:
    adc_delay: float = 0.01


class PWMTheremin:
    def __init__(
        self,
        hardware_information: Optional[HardwareInformation] = HardwareInformation(),
        parameter_configuration: Optional[ParameterConfiguration] = ParameterConfiguration(),
    ) -> None:
        self.hardware_information = hardware_information

        self.parameter_configuration = parameter_configuration

        self.adc = ADC(Pin(hardware_information.adc_gpio_pin))

        self.speaker_pwm = PWM(Pin(0), freq=1000, duty_u16=32768)

    async def read_adc_values_loop(self, sample_value_reader, sample_value_consumer):

        while True:
            raw_adc_value = sample_value_reader()
            sample_value_consumer(raw_adc_value)
            await asyncio.sleep(self.parameter_configuration.adc_delay)

    async def main(self):
        await self.read_adc_values_loop(
            sample_value_reader=self.adc.read_u16,
            sample_value_consumer=self.set_value,
        )

    def get_frequency_value(self, raw_adc_value: int) -> int:
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

    def set_value(self, raw_adc_value):
        frequency_value = self.get_frequency_value(raw_adc_value)
        if frequency_value > self.hardware_information.miminum_pwm_frequency:
            self.speaker_pwm.freq(int(frequency_value))

        print(f"{raw_adc_value} -> {frequency_value}\n")


if __name__ == "__main__":
    theremin = PWMTheremin()
    asyncio.run(theremin.main())  #  type: ignore
