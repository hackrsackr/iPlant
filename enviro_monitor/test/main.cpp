#include "Arduino.h"
#include <Adafruit_ADS1X15.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>
#include "Adafruit_VEML7700.h"

#include "config.hpp"
#include "ADS_Sensor.hpp"

#include <string>

std::vector<ADS_Sensor *> _ADCS;

Adafruit_BME280 bme;
Adafruit_VEML7700 veml = Adafruit_VEML7700();

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
      
    if (!veml.begin()) {
    Serial.println("Sensor not found");
    while (1);
    }

    Serial.println("Sensor found");
    
    veml.setLowThreshold(10000);
    veml.setHighThreshold(20000);
    veml.interruptEnable(true);
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
    
    Serial.printf("ALS: %2.2f \n", veml.readALS());
    Serial.printf("White: %2.2f \n", veml.readWhite());
    Serial.printf("Lux: %2.2f \n", veml.readLux(VEML_LUX_CORRECTED));
    
    Serial.println("------------------------------------------");
    delay(_DELAY_MILLISECONDS);
}