#include <Arduino.h>
#include <notes.h>
#include "hardware/gpio.h"

unsigned int PIN_DOWN = 16;
unsigned int PIN_UP = 17;

unsigned long KEY_DEBOUNCE_DELAY_US = 100000;
unsigned long last_press_time = 0;

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

void setNoteNumber(unsigned int i, unsigned int note_number)
{
  notes[i].note_number = note_number;
  initializeNoteDelaysFromFrequency();
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

    if (pitch_up && current - last_press_time > KEY_DEBOUNCE_DELAY_US)
    {
      setNoteNumber(i, newNoteNumberUp(notes[i].note_number));
      last_press_time = current;
    }

    if (pitch_down && current - last_press_time > KEY_DEBOUNCE_DELAY_US)
    {
      setNoteNumber(i, newNoteNumberDown(notes[i].note_number));
      last_press_time = current;
    }

    if ((current - notes[i].lastTick > notes[i].delayTimeus) && play_note)
    {
      notes[i].status = !notes[i].status;
      gpio_put(notes[i].pin, notes[i].status);
      notes[i].lastTick = current;
    }
  }
}
