#include <unity.h>
#include <Arduino.h>
#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

void setUp(void)
{
    // set stuff up here
}

void tearDown(void)
{
    // clean stuff up here
}

void simple_test(void)
{
    TEST_ASSERT_EQUAL(33, 33);
    TEST_ASSERT_EQUAL(1, 1);
}

void setup()
{
    delay(2000);

    UNITY_BEGIN();
    RUN_TEST(simple_test);
    UNITY_END();
}

void loop()
{
    delay(1000);
}