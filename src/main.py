from machine import ADC, Pin, I2C  # type: ignore

import asyncio


class HardwareInformation:
    adc_gpio_pin = 26
    pwm_pin = 4


class ParameterConfiguration:
    adc_delay: float = 0.01


class PWMTheremin:
    def __init__(
        self,
        hardware_information: HardwareInformation = HardwareInformation(),
        parameter_configuration: ParameterConfiguration = ParameterConfiguration(),
    ):
        self.hardware_information = hardware_information

        self.parameter_configuration = parameter_configuration

        self.adc = ADC(Pin(hardware_information.adc_gpio_pin))

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

    def set_value(self, value):
        print(f"{value}\n")


if __name__ == "__main__":
    theremin = PWMTheremin()
    asyncio.run(theremin.main())  #  type: ignore
