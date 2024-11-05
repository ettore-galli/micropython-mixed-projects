#include <Arduino.h>

int LED{15};
int BLINK_DELAY{300};

void setup()
{
    pinMode(LED, OUTPUT);
    Serial.begin(9600);
}

void switchLed(int led, int delayTime, PinStatus status)
{
    digitalWrite(led, status);
    Serial.print("status [");
    Serial.print(status);
    Serial.print("] \n");
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

void sweepDelayLoop()
{
    int delay_base = 100;
    int delay_step = 100;
    int delay = delay_base;
    while (true)
    {

        switchLedOn(LED, delay);
        switchLedOff(LED, delay);

        delay += delay_step;
        if (delay < delay_base || delay > 10 * delay_base)
        {
            delay_step = -delay_step;
        }
    }
}

void loop()
{
    sweepDelayLoop();
}