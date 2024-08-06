# Micropython ESP8266

Future porting of this project

## Reference

<https://docs.micropython.org/en/latest/esp8266/tutorial/intro.html>

## Install micropython

```shell
pip install esptool
```

```shell
export UPORT=$(ls -1 /dev/* | grep tty.usbserial | head)
esptool.py --port "${UPORT}" erase_flash
esptool.py --port "${UPORT}" --baud 460800 write_flash --flash_size=detect 0 firmware/ESP8266_GENERIC-20240602-v1.23.0.bin

```
