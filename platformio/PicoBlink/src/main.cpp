#include <Arduino.h>
#include "blink_logic.h"

int LED{15};
int BLINK_DELAY{300};

void setup()
{
  pinMode(LED, OUTPUT);
  Serial.begin(9600);
}

void switchLed(int led, int delayTime, int status)
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

void loop()
{
  sweepDelayLoop(&LED, &switchLedOn, &switchLedOff);
}