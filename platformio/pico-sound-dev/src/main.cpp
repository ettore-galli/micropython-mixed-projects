#include <Arduino.h>
#include <notes.h>

void setup()
{
  Serial.begin(9600);
  Serial.println("Setup...");
  int microseconds = 1000000;
  for (unsigned int i = 0; i < NUMBER_OF_NOTES; i++)
  {
    pinMode(notes[i].pin, OUTPUT);
    notes[i].delayTimeus = 2 * int(microseconds / notes[i].freq);
    Serial.println(notes[i].delayTimeus);
  }
}

void loop()
{
  unsigned long current = micros();

  for (unsigned int i = 0; i < NUMBER_OF_NOTES; i++)
  {

    if (current - notes[i].lastTick > notes[i].delayTimeus)
    {
      notes[i].status = !notes[i].status;
      gpio_put(notes[i].pin, notes[i].status);
      notes[i].lastTick = current;
    }
  }
}
