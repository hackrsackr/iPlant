#include "Arduino.h"
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>

// #include "config.hpp"

#include <string>

constexpr auto BME_I2C_ADDR(0x76);
constexpr auto I2C_SCL(17);
constexpr auto I2C_SDA(18);
constexpr auto SEALEVELPRESSURE_HPA(1013.25);
constexpr auto DELAY_MILLISECONDS(2000);

Adafruit_BME280 bme; // I2C

void setup()
{
    Serial.begin(115200);
    Serial.println(F("BME280 test"));

    Wire.begin(I2C_SDA, I2C_SCL);

    if (!bme.begin(BME_I2C_ADDR, &Wire))
    {
        Serial.println("Could not find a valid BME280 sensor, check wiring!");
    }
}

void printValues()
{
    Serial.printf("TempC: %2.2f *C\n", bme.readTemperature());
    Serial.printf("TempF: %2.2f *F\n", (1.8 * bme.readTemperature() + 32));
    Serial.printf("Pressure: %4.2f mBar\n", bme.readPressure() / 100.0);
    Serial.printf("Altitude: %3.2f m\n", bme.readAltitude(SEALEVELPRESSURE_HPA));
    Serial.printf("Humidity: %2.2f %%\n", bme.readHumidity());
    Serial.println();
}

void loop()
{
    printValues();
    // Serial.printf("TempC: %2.2f *C\n", bme.readTemperature());
    // Serial.println(bme.readTemperature());
    delay(DELAY_MILLISECONDS);
}