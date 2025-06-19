import asyncio

from control_demo_engine import ControlDemoEngine  # type: ignore[import-not-found]
from hardware import HardwarePin, HardwareTime, SerialCommunicator  # type: ignore[import-untyped]

if __name__ == "__main__":
    control_demo = ControlDemoEngine(
        time=HardwareTime(),
        pin_class=HardwarePin,
        serial_communicator_class=SerialCommunicator,
    )
    asyncio.run(control_demo.main())
