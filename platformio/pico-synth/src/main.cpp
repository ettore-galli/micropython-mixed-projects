#include <Arduino.h>
#include <notes.h>
#include <analog.h>
#include "hardware/gpio.h"

typedef unsigned int (*NoteNumberChangeFunction)(const unsigned int note_number);

SimpleAnalog adc(A0, 8);

const unsigned int NUMBER_OF_HARMONICS = 2;

note synth_note[NUMBER_OF_HARMONICS] = {
    {0, 0, 0, 0, false},
    {0, 1, 0, 0, false},
};

unsigned long adc_last_tick = 0;
unsigned int current_note_number = 0;

void initializeAdcPin()
{
}

void initializeOutputPins()
{
  for (unsigned int i = 0; i < NUMBER_OF_HARMONICS; i++)
  {
    pinMode(synth_note[i].pin, OUTPUT);
  }
}

unsigned int calculateDelayMicroseconds(float frequency)
{
  int microseconds = 1000000;
  return 2 * int(microseconds / frequency);
}

void initializeNoteDelayFromFrequency()
{
  synth_note[0].delayTimeus = calculateDelayMicroseconds(notes_reference[synth_note[0].note_number].freq);
  for (unsigned int i = 1; i < NUMBER_OF_HARMONICS; i++)
  {
    synth_note[i].delayTimeus = synth_note[0].delayTimeus * 2;
  }
}

void setNoteNumber(unsigned int note_number)
{
  for (unsigned int i = 0; i < NUMBER_OF_HARMONICS; i++)
  {
    synth_note[i].note_number = note_number;
    synth_note[i].status = false;
    synth_note[i].lastTick = 0;
  }
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

  if (current - adc_last_tick > 100000)
  {
    short read = adc.analogRead8();
    current_note_number = getNoteNumberFromAdcRead(read);

    if (current_note_number != synth_note[0].note_number)
    {
      setNoteNumber(current_note_number);
    }
    adc_last_tick = current;
  }

  uint32_t play_note = current_note_number > 0;

  if (play_note)
  {

    if (current - synth_note[NUMBER_OF_HARMONICS - 1].lastTick > synth_note[NUMBER_OF_HARMONICS - 1].delayTimeus)
    {
      for (unsigned int i = 0; i < NUMBER_OF_HARMONICS; i++)
      {
        synth_note[i].status = !synth_note[i].status;
        gpio_put(synth_note[i].pin, synth_note[i].status);
        synth_note[i].lastTick = current;
      }
    }
    else
    {
      for (unsigned int i = 0; i < NUMBER_OF_HARMONICS; i++)
      {
        if (current - synth_note[i].lastTick > synth_note[i].delayTimeus)

        {
          synth_note[i].status = !synth_note[i].status;
          gpio_put(synth_note[i].pin, synth_note[i].status);
          synth_note[i].lastTick = current;
        }
      }
    }
  }
}
