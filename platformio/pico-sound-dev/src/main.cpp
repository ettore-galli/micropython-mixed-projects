#include <Arduino.h>
#include <notes.h>
#include "hardware/gpio.h"

void initializeInputPins()
{
  for (unsigned int i = 0; i < ACTUAL_NUMBER_OF_NOTES; i++)
  {
    pinMode(control_pins[i].control_pin, INPUT_PULLUP);
  }
}

void initializeOutputPins()
{
  for (unsigned int i = 0; i < ACTUAL_NUMBER_OF_NOTES; i++)
  {
    pinMode(notes[i].pin, OUTPUT);
  }
}

unsigned int calculateDelayMicroseconds(float frequency)
{
  int microseconds = 1000000;
  return 2 * int(microseconds / frequency);
}

void initializeNoteDelaysFromFrequency()
{
  for (unsigned int i = 0; i < ACTUAL_NUMBER_OF_NOTES; i++)
  {
    notes[i].delayTimeus = calculateDelayMicroseconds(notes_reference[notes[i].note_number].freq);
  }
}

void setup()
{
  initializeInputPins();
  initializeOutputPins();
  initializeNoteDelaysFromFrequency();
}

void loop()
{

  unsigned long current = micros();

  for (unsigned int i = 0; i < ACTUAL_NUMBER_OF_NOTES; i++)
  {
    unsigned int control_pin = control_pins[i].control_pin;

    uint32_t control_pin_state = gpio_get(control_pin);

    if ((current - notes[i].lastTick > notes[i].delayTimeus) && (control_pin_state == LOW))
    {
      notes[i].status = !notes[i].status;
      gpio_put(notes[i].pin, notes[i].status);
      notes[i].lastTick = current;
    }
  }
}
