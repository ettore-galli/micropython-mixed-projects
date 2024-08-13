import asyncio
from collections.abc import Callable
from typing import ClassVar

from machine import ADC, PWM, Pin  # type: ignore[import-not-found]


class HardwareInformation:
    pitch_adc_gpio_pin: int = 26
    set_adc_gpio_pin: int = 27
    speaker_pwm_pins: ClassVar[list[int]] = [0, 2, 4]

    miminum_pwm_frequency = 20


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

        self.pitch_adc = ADC(Pin(self.hardware_information.pitch_adc_gpio_pin))
        self.set_adc = ADC(Pin(self.hardware_information.set_adc_gpio_pin))

        self.set_pwm_on(freq=1000)

    def set_pwm_off(self) -> None:
        for speaker_pwm in self.speaker_pwms:
            speaker_pwm.deinit()

    def set_pwm_on(self, freq: int) -> None:
        self.speaker_pwms = [
            PWM(
                Pin(pwm_pin),
                freq=freq,
                duty_u16=32768,
            )
            for pwm_pin in self.hardware_information.speaker_pwm_pins
        ]
        self.set_pwm_freq(freq=freq)

    def set_pwm_freq(self, freq: int) -> None:
        self.speaker_pwms[0].freq(freq)
        self.speaker_pwms[1].freq(int(freq * 2))
        self.speaker_pwms[2].freq(int(freq * 3))

    async def read_adc_values_loop(
        self,
        sample_value_reader: Callable[[], int],
        set_value_reader: Callable[[], int],
        sample_value_consumer: Callable[[int, int], None],
    ) -> None:

        while True:
            raw_adc_value = sample_value_reader()
            raw_set_value = set_value_reader()
            sample_value_consumer(raw_adc_value, raw_set_value)
            await asyncio.sleep(self.parameter_configuration.adc_delay)

    async def main(self) -> None:
        await self.read_adc_values_loop(
            sample_value_reader=self.pitch_adc.read_u16,
            set_value_reader=self.set_adc.read_u16,
            sample_value_consumer=self.set_value,
        )

    def get_frequency_value(self, raw_adc_value: int) -> float:
        return self.hardware_information.miminum_pwm_frequency + int(raw_adc_value / 16)

    def set_value(self, raw_adc_value: int, raw_set_value: int) -> None:
        frequency_value = self.get_frequency_value(raw_adc_value)
        if raw_adc_value > raw_set_value:
            self.set_pwm_freq(int(frequency_value))
        else:
            self.set_pwm_off()


if __name__ == "__main__":
    theremin = PWMTheremin()
    asyncio.run(theremin.main())
