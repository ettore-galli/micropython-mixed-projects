from machine import ADC, Pin, PWM  # type: ignore

import asyncio


class HardwareInformation:
    adc_gpio_pin: int = 26
    speaker_pwm_pin: int = 0
    miminum_pwm_frequency = 20


class ParameterConfiguration:
    adc_delay: float = 0.005


class PWMTheremin:
    def __init__(
        self,
        hardware_information: HardwareInformation = HardwareInformation(),
        parameter_configuration: ParameterConfiguration = ParameterConfiguration(),
    ):
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

    def set_value(self, raw_adc_value):
        frequency_value = raw_adc_value / 16
        if frequency_value > self.hardware_information.miminum_pwm_frequency:
            self.speaker_pwm.freq(int(frequency_value))

        print(f"{frequency_value}\n")


if __name__ == "__main__":
    theremin = PWMTheremin()
    asyncio.run(theremin.main())  #  type: ignore
