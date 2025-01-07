#include <Arduino.h>
#include <notes.h>
#include <analog.h>
#include "hardware/gpio.h"

typedef unsigned int (*NoteNumberChangeFunction)(const unsigned int note_number);

SimpleAnalog adc(A0, 8);

SynthNote synthNote = {0, {0, 1}, 0, 0, false, 0};

unsigned long adc_last_tick = 0;
unsigned int current_note_number = 0;

void initializeAdcPin()
{
}

void initializeOutputPins()
{
  for (unsigned int i = 0; i < NUMBER_OF_OUTPUT_PINS; i++)
  {
    pinMode(synthNote.pins[i], OUTPUT);
  }
}

unsigned int calculateDelayMicroseconds(float frequency)
{
  int microseconds = 1000000;
  return 2 * int(microseconds / frequency);
}

void initializeNoteDelayFromFrequency()
{
  synthNote.delayTimeus = calculateDelayMicroseconds(notes_reference[synthNote.note_number].freq) / NUMBER_OF_OUTPUT_PINS;
}

void setNoteNumber(unsigned int note_number)
{

  synthNote.note_number = note_number;
  synthNote.status = false;
  synthNote.lastTick = 0;

  initializeNoteDelayFromFrequency();
}

void setup()
{
  initializeAdcPin();
  initializeOutputPins();
  initializeNoteDelayFromFrequency();
}

unsigned int getNoteNumberFromAdcRead(short adcRead)
{
  return int(adcRead / (adc.ADC_MAX / TOTAL_NUMBER_OF_NOTES));
}

void loop()
{

  unsigned long current = micros();

  if (current - adc_last_tick > 1000)
  {
    short read = adc.analogRead8();
    current_note_number = getNoteNumberFromAdcRead(read);

    if (current_note_number != synthNote.note_number)
    {
      setNoteNumber(current_note_number);
    }
    adc_last_tick = current;
  }

  uint32_t play_note = current_note_number > 0;

  if (play_note)
  {
    if (current - synthNote.lastTick > synthNote.delayTimeus)
    {
      nextSynthNoteStatus(&synthNote);
      setSynthNotePinStatus(&synthNote);
      for (unsigned int p = 0; p < NUMBER_OF_OUTPUT_PINS; p++)
      {
        gpio_put(synthNote.pins[p], synthNote.pin_status[p]);
      }
      synthNote.lastTick = current;
    }
  }
}
