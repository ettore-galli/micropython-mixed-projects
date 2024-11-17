#include <string>
#include <display_device.h>
#include <display_base.h>

class SignalPloter
{
public:
    int16_t _samples{SCREEN_WIDTH};
    int16_t _x;
    int16_t _values[SCREEN_WIDTH];
    DisplayDevice _display;

    SignalPloter(DisplayDevice display) : _x(0), _display(display)
    {
        _x = 0;
        _display = display;
    };

    void displayValuesChunk()
    {
        display.clearDisplay();
        for (int16_t x = 0; x < SCREEN_WIDTH; ++x)
        {
            display.drawPixel(x, _values[x], SSD1306_WHITE);
        }
        display.display();
    }
    void pushValue(int16_t v)
    {
        _x++;
        if (_x > _samples)
        {
            displayValuesChunk();
            _x = 0;
        }
        _values[_x] = v;
    };
};

void displaySetup();

void printString(int16_t x, int16_t y, std::string message, int size);

void displayValueBar(int value);