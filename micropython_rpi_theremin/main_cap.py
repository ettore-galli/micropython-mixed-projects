from collections.abc import Callable

import utime  # type: ignore[import-not-found]
from machine import ADC, PWM, Pin  # type: ignore[import-not-found]


class HardwareInformation:
    adc_gpio_pin: int = 26
    pwm_gen_pin: int = 0


class ParameterConfiguration:
    adc_delay_ms: int = 20


class PWMCapSensor:
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

        self.pwm = PWM(
            Pin(self.hardware_information.pwm_gen_pin),
            freq=8,
            duty_u16=32768,
        )

    def read_adc_values_loop(
        self,
        sample_value_reader: Callable[[], int],
        sample_value_consumer: Callable[[int], None],
    ) -> None:

        while True:
            raw_adc_value = sample_value_reader()
            sample_value_consumer(raw_adc_value)
            utime.sleep_ms(self.parameter_configuration.adc_delay_ms)

    def notify_value(self, value: int) -> None:
        print("*" * int(value / 1024))

    def main(self) -> None:
        self.read_adc_values_loop(
            sample_value_reader=self.adc.read_u16,
            sample_value_consumer=self.notify_value,
        )


if __name__ == "__main__":
    cap_sensor = PWMCapSensor()
    cap_sensor.main()
