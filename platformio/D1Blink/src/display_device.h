
#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <string>

class DisplayDevice : public Adafruit_SSD1306
{
public:
  DisplayDevice(uint8_t w, uint8_t h, TwoWire *twi = &Wire,
                int8_t rst_pin = -1) : Adafruit_SSD1306(w, h, twi, rst_pin) {}
};

extern DisplayDevice display;