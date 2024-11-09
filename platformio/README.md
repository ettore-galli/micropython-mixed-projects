
This directory is intended for PlatformIO Test Runner and project tests.

Unit Testing is a software testing method by which individual units of
source code, sets of one or more MCU program modules together with associated
control data, usage procedures, and operating procedures, are tested to
determine whether they are fit for use. Unit testing finds problems early
in the development cycle.

More information about PlatformIO Unit Testing:

- <https://docs.platformio.org/en/latest/advanced/unit-testing/index.html>

## Various

- Fix tests
<https://community.platformio.org/t/cannot-build-tests/22066/2>
<https://github.com/platformio/platformio-core/issues/3980>

```bash
pio upgrade --dev
```

## Fix unit tests double definition problem

<https://community.platformio.org/t/cannot-build-tests/22066/2>

```bash
/Users/ettoregalli/.platformio/packages/framework-arduino-mbed/variants/RASPBERRY_PI_PICO/libs
# uncompress libmbed.a
# rename 
ar -r libmbed.a libmbed/*.*
```

## Fix unit tests double definition problem custom config

<https://docs.platformio.org/en/latest/advanced/unit-testing/frameworks/custom/examples/custom_unity_library.html>
<https://community.platformio.org/t/no-output-in-pio-cli-when-unit-testing/24006>
<https://community.platformio.org/t/teensy-4-1-unit-testing-issue/21033/5>
<https://github.com/platformio/platformio-core/issues/3742>
