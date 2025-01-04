#include "Arduino.h"
#include "pins_arduino.h"
#include "pinDefinitions.h"

class SimpleAnalog
{

public:
    static const unsigned int ADC_MAX = 255;
    pin_size_t _pin;
    int _read_resolution;
    mbed::AnalogIn *_adc;

    SimpleAnalog(const pin_size_t pin, const int read_resolution)
    {
        _pin = pin;
        _read_resolution = read_resolution;

        PinName name = analogPinToPinName(_pin);
        _adc = new mbed::AnalogIn(name);
        analogPinToAdcObj(pin) = _adc;
        if (_adc == NULL)
        {
            _adc = new mbed::AnalogIn(name);
            analogPinToAdcObj(pin) = _adc;
#ifdef ANALOG_CONFIG
            if (isAdcConfigChanged)
            {
                _adc->configure(adcCurrentConfig);
            }
#endif
        }
    };

    ~SimpleAnalog() {};

    int analogRead8()
    {
        return (_adc->read_u16() >> (16 - 8));
    };
};