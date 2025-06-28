import asyncio

from control_demo_engine import ControlDemoEngine  # type: ignore[import-not-found, import-untyped]
from control_demo_hardware import (  # type: ignore[import-not-found, import-untyped]
    AccessPoint,
    HardwarePin,
    HardwareTime,
    WifiClient,
    retrieve_wifi_client_information,
)
from control_demo_server import WebServer  # type: ignore[import-not-found, import-untyped]

if __name__ == "__main__":
    control_demo = ControlDemoEngine(
        time=HardwareTime(),
        pin_class=HardwarePin,
        access_point_class=AccessPoint,
        wifi_client_class=WifiClient,
        wifi_client_information_retriever=retrieve_wifi_client_information,
        web_server_class=WebServer,
    )
    asyncio.run(control_demo.main())
