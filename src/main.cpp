#include "Arduino.h"
#include <Adafruit_ADS1X15.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>

#include "config.hpp"
#include "ADS_Sensor.hpp"

#include <string>

std::vector<ADS_Sensor *> _ADCS;

Adafruit_BME280 bme;

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
    
    if (!bme.begin(_BME_I2C_ADDR, &Wire))
    {
        Serial.println("Could not find a valid BME280 sensor, check wiring!");
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
    
    // Serial.printf("TempC: %2.2f *C\n", bme.readTemperature());
    Serial.printf("Temperature: %2.2f *F \t \n", (1.8 * bme.readTemperature() + 32));
    Serial.printf("Humidity: %2.2f %%\n", bme.readHumidity());
    
    Serial.println("------------------------------------------");
    
    delay(_DELAY_MILLISECONDS);
}