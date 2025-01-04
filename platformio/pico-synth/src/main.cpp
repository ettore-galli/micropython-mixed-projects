#include <Arduino.h>
#include <notes.h>
#include <analog.h>
#include "hardware/gpio.h"

typedef unsigned int (*NoteNumberChangeFunction)(const unsigned int note_number);

SimpleAnalog adc(A0, 8);

void initializeAdcPin()
{
}

void initializeOutputPins()
{
  pinMode(synth_note.pin, OUTPUT);
}

unsigned int calculateDelayMicroseconds(float frequency)
{
  int microseconds = 1000000;
  return 2 * int(microseconds / frequency);
}

void initializeNoteDelayFromFrequency()
{
  synth_note.delayTimeus = calculateDelayMicroseconds(notes_reference[synth_note.note_number].freq);
}

void setNoteNumber(unsigned int note_number)
{
  synth_note.note_number = note_number;
  initializeNoteDelayFromFrequency();
}

void setup()
{

  Serial.begin(9600);

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
  short read = adc.analogRead8();
  unsigned int note_number = getNoteNumberFromAdcRead(read);

  if (note_number != synth_note.note_number)
  {
    Serial.print(read);
    Serial.print(" / ");
    Serial.print(TOTAL_NUMBER_OF_NOTES);
    Serial.print(" = ");
    Serial.println(note_number);

    setNoteNumber(note_number);
  }

  unsigned long current = micros();
  uint32_t play_note = note_number > 0;

  if ((current - synth_note.lastTick > synth_note.delayTimeus) && play_note)
  {
    synth_note.status = !synth_note.status;
    gpio_put(synth_note.pin, synth_note.status);
    synth_note.lastTick = current;
  }
}
