#include <Arduino.h>
#include "blink_logic.h"
#include <string>
#include "display.h"

int LED{15};
int BLINK_DELAY{300};

void setup()
{
  displaySetup();
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
  // sweepDelayLoop(&LED, &switchLedOn, &switchLedOff);
  // display_loop();
  //printString(0, 0,  std::to_string(analogRead(A0/32)), 4);
  displayValueBar(analogRead(A0/32));
  // for (int i=0; i<64; ++i){
  //     std::string message{"print"};
  //     printString(0, 0,  std::to_string(i), 4);
  // }

}