from collections.abc import Callable

import utime  # type: ignore[import-not-found]
from machine import ADC, PWM, Pin  # type: ignore[import-not-found]


class HardwareInformation:
    pitch_adc_gpio_pin: int = 26
    set_adc_gpio_pin: int = 27
    speaker_pwm_pin: int = 0


class ParameterConfiguration:
    adc_delay_ms: int = 100


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
        self.speaker_pwm.deinit()

    def set_pwm_on(self, freq: int) -> None:
        self.speaker_pwm: PWM = PWM(
            Pin(self.hardware_information.speaker_pwm_pin),
            freq=freq,
            duty_u16=32768,
        )

    def read_adc_values_loop(
        self,
        sample_value_reader: Callable[[], int],
        set_value_reader: Callable[[], int],
        sample_value_consumer: Callable[[int, int], None],
    ) -> None:

        while True:
            raw_adc_value = sample_value_reader()
            raw_set_value = set_value_reader()
            sample_value_consumer(raw_adc_value, raw_set_value)
            utime.sleep_us(self.parameter_configuration.adc_delay_ms)

    def main(self) -> None:
        self.read_adc_values_loop(
            sample_value_reader=self.pitch_adc.read_u16,
            set_value_reader=self.set_adc.read_u16,
            sample_value_consumer=self.set_value,
        )

    def get_frequency_value(self, raw_adc_value: int, raw_set_value: int) -> float:
        return 8 + int((raw_set_value - raw_adc_value) / 8)

    def set_pwm_freq(self, freq: int) -> None:
        self.speaker_pwm.freq(freq)

    def set_value(self, raw_adc_value: int, raw_set_value: int) -> None:
        frequency_value = self.get_frequency_value(raw_adc_value, raw_set_value)
        if raw_adc_value < raw_set_value:
            self.set_pwm_freq(int(frequency_value))
        else:
            self.set_pwm_off()


if __name__ == "__main__":
    theremin = PWMTheremin()
    theremin.main()
