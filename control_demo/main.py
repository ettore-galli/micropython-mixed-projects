import asyncio

from control_demo_engine import ControlDemoEngine  # type: ignore[import-not-found]
from control_demo_hardware import AccessPoint, HardwarePin, HardwareTime  # type: ignore[import-not-found]

if __name__ == "__main__":
    control_demo = ControlDemoEngine(
        time=HardwareTime(),
        pin_class=HardwarePin,
        access_point_class=AccessPoint,
    )
    asyncio.run(control_demo.main())
