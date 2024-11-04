# Arduino CLI

## Setup

Various references:

<https://arduino.github.io/arduino-cli/1.0/getting-started/>

<https://learn.sparkfun.com/tutorials/efficient-arduino-programming-with-arduino-cli-and-visual-studio-code/all>

### Download latest release, e.g

<https://github.com/arduino/arduino-cli/releases/tag/v1.0.4>

### Put into a convenient directory and call accordingly (or add to path)

```~/arduino-cli/arduino-cli```

```shell
export PATH=$PATH:~/arduino-cli
```

### Known locations

```shell
# Config file
/Users/ettoregalli/Library/Arduino15/arduino-cli.yaml

# Hardware
/Users/ettoregalli/Library/Arduino15/packages/arduino/*
```

### Configuration file

```shell
arduino-cli config init
Config file written to: /Users/ettoregalli/Library/Arduino15/arduino-cli.yaml
```

### Install driver (e.g. rp2040 aka Raspberry pi pico)

<https://forum.arduino.cc/t/how-to-use-pico-with-arduino-cli/1015586/2>

```shell
arduino-cli core update-index
arduino-cli core install arduino:mbed_rp2040

You might need to configure permissions for uploading.
To do so, run the following command from the terminal:
sudo "/Users/ettoregalli/Library/Arduino15/packages/arduino/hardware/mbed_rp2040/4.1.5/post_install.sh"
```

### Compile/Upload

```shell
arduino-cli compile --upload --verbose --fqbn arduino:mbed_rp2040:pico Blink/Blink.ino --port /dev/cu.usbmodem11401
```
