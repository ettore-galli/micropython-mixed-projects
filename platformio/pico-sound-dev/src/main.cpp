#include <Arduino.h>

struct note
{
  unsigned long lastTick;
  uint pin;
  uint delayTimeus;
  bool status;
};

note notes[] = {
    {0, 16, 2272, false},
    {0, 17, 1607, false}};

void setup()
{

  for (int i = 0; i < 2; i++)
  {
    pinMode(notes[i].pin, OUTPUT);
  }
}

void loop()
{
  unsigned long current = micros();

  for (int i = 0; i < 2; i++)
  {

    if (current - notes[i].lastTick > notes[i].delayTimeus)
    {
      notes[i].status = !notes[i].status;
      digitalWrite(notes[i].pin, notes[i].status);
      notes[i].lastTick = current;
    }
  }
}
