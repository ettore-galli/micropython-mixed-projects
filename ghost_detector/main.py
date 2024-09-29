from ghost_detector_logic import GhostDetector  # type: ignore[import-not-found]
from hardware import MachineADC, sleep_ms  # type: ignore[import-not-found]

if __name__ == "__main__":
    ghost_detector = GhostDetector(adc_class=MachineADC, sleep_ms=sleep_ms)
    ghost_detector.main()
