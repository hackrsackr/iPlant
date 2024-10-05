#pragma once

#include <Adafruit_ADS1X15.h>

#include <memory>
#include <string>

typedef struct ads_sensor_cfg_t
{
    uint8_t i2c_addr;
    uint8_t ads_channel;
    adsGain_t ads_gain;
    std::string ads_sensor_unit;
    float input_low_val;
    float input_high_val;
    float output_low_val;
    float output_high_val;
} ads_sensor_cfg_t;

class ADS_Sensor
{

public:
    ADS_Sensor(ads_sensor_cfg_t);
    ~ADS_Sensor();

    bool begin();
    auto getSensorUnitType() -> std::string;
    uint8_t getSensorChannel();
    auto readADC() -> uint16_t;
    auto readVolts() -> float;
    auto readSensorUnits() -> float;

private:
    std::shared_ptr<Adafruit_ADS1115> _p_ads;
    uint8_t _i2c_addr;
    uint8_t _ads_channel;
    std::string _ads_sensor_unit;
    float _input_low_val;
    float _input_high_val;
    float _output_low_val;
    float _output_high_val;
};