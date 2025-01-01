#include <Arduino.h>
#include <notes.h>
#include "hardware/gpio.h"

unsigned int PIN_DOWN = 16;
unsigned int PIN_UP = 17;

unsigned int SET_KEY_DELAY_MS = 100;

typedef unsigned int (*NoteNumberChangeFunction)(const unsigned int note_number);

void initializeInputPins()
{
  for (unsigned int i = 0; i < ACTUAL_NUMBER_OF_NOTES; i++)
  {
    pinMode(control_pins[i].control_pin, INPUT_PULLUP);
  }
  for (unsigned int pin : {PIN_DOWN, PIN_UP})
  {
    pinMode(pin, INPUT_PULLUP);
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



void pitchChange(NoteNumberChangeFunction note_number_change)
{
  for (unsigned int i = 0; i < ACTUAL_NUMBER_OF_NOTES; i++)
  {
    unsigned int control_pin = control_pins[i].control_pin;

    uint32_t control_pin_state = gpio_get(control_pin);

    if (control_pin_state == LOW)
    {
      notes[i].note_number = note_number_change(notes[i].note_number);
      initializeNoteDelaysFromFrequency();
    }
  }
}

void pitchUp()
{
  pitchChange(newNoteNumberUp);
}

void pitchDown()
{
  pitchChange(newNoteNumberDown);
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
  uint32_t up_pin_state = gpio_get(PIN_UP);
  uint32_t down_pin_state = gpio_get(PIN_DOWN);

  for (unsigned int i = 0; i < ACTUAL_NUMBER_OF_NOTES; i++)
  {
    unsigned int control_pin = control_pins[i].control_pin;

    uint32_t control_pin_state = gpio_get(control_pin);

    uint32_t play_note = (control_pin_state == LOW) && (up_pin_state == HIGH) && (down_pin_state == HIGH);
    uint32_t pitch_up = (control_pin_state == LOW) && (up_pin_state == LOW) && (down_pin_state == HIGH);
    uint32_t pitch_down = (control_pin_state == LOW) && (up_pin_state == HIGH) && (down_pin_state == LOW);

    if ((current - notes[i].lastTick > notes[i].delayTimeus) && play_note)
    {
      notes[i].status = !notes[i].status;
      gpio_put(notes[i].pin, notes[i].status);
      notes[i].lastTick = current;
    }
    if (pitch_up)
    {
      pitchUp();
      delay(SET_KEY_DELAY_MS);
    }
    if (pitch_down)
    {
      pitchDown();
      delay(SET_KEY_DELAY_MS);
    }
  }
}
