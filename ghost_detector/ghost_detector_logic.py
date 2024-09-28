from collections.abc import Callable
from math import cos

from base import BaseADC  # type: ignore[import-untyped]


class HardwareInformation:
    adc_pin: int = 0


class ParameterConfiguration:
    adc_delay_ms: int = 25


class GhostDetector:
    def __init__(
        self,
        adc_class: type[BaseADC],
        sleep_ms: Callable[[float], None],
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

        self.adc_class: type[BaseADC] = adc_class
        self.sleep_ms = sleep_ms

        self.adc = self.adc_class(self.hardware_information.adc_pin)

    def read_adc_values_loop(
        self,
        sample_value_reader: Callable[[], int],
        sample_value_consumer: Callable[[int], None],
    ) -> None:

        while True:

            raw_adc_value = sample_value_reader()
            sample_value_consumer(raw_adc_value)
            self.sleep_ms(self.parameter_configuration.adc_delay_ms)

    @staticmethod
    def perform_r_dft(samples: list[float]) -> list[float]:
        def r_dft_term(n_samples: float, sample: float, nth_freq: float) -> float:
            return sum(
                sample * cos(6.28 * index * nth_freq / n_samples) / 1024.0
                for index in range(int(n_samples))
            )

        return [
            r_dft_term(len(samples), sample, index)
            for index, sample in enumerate(samples)
        ]

    def notify_value(self, value: int) -> None:
        stars = int(value / 1024)
        lines = 64 - stars
        print("#" * stars + ":" * lines)  # noqa: T201

    def main(self) -> None:
        self.read_adc_values_loop(
            sample_value_reader=self.adc.read_u16,
            sample_value_consumer=self.notify_value,
        )
