#include <Common.h>
#include <pins_arduino.h>
#include <iostream>

using std::cout;

int LED{15};
int BLINK_DELAY{300};

void setup()
{
    pinMode(LED, OUTPUT);
}

void switchLed(int led, int delayTime, PinStatus status)
{
    digitalWrite(led, status);
    cout << "status: " << status << "\n";
    delay(delayTime);
};

void switchLedOn(int led, int delayTime)
{
    switchLed(led, delayTime, HIGH);
}

void switchLedOff(int led, int delayTime)
{
    switchLed(led, delayTime, LOW);
}

void loop()
{

    switchLedOn(LED, BLINK_DELAY);
    switchLedOff(LED, BLINK_DELAY);
}