#include "Arduino.h"
#include <Adafruit_ADS1X15.h>

#include "config.hpp"
#include "ADS_Sensor.hpp"

#include <string>

std::vector<ADS_Sensor *> _ADCS;

void setup(void)
{
    Serial.begin(115200);
    Wire.begin(_I2C_SDA, _I2C_SCL);

    for (auto &ads_cfg : ads_cfgs)
    {
        ADS_Sensor *a = new ADS_Sensor(ads_cfg);
        _ADCS.push_back(a);

        if (!a->begin())
        {
            Serial.printf("ads failed to initialize");
        }
    }
}

void loop(void)
{
    for (auto &ADC : _ADCS)
    {
        Serial.printf("ADC%i: %6d \t", ADC->getSensorChannel(), ADC->readADC());
        Serial.printf("VOLTS%i: %1.2f \t", ADC->getSensorChannel(), ADC->readVolts());
        Serial.printf("%s%i: %2.2f \n", ADC->getSensorUnitType().c_str(), ADC->getSensorChannel(), ADC->readSensorUnits());
    }
    Serial.println("------------------------------------------");
    delay(1000);
}