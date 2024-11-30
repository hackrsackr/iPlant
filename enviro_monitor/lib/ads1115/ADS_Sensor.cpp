#include "ADS_Sensor.hpp"

#include "config.h"

ADS_Sensor::ADS_Sensor(ads_sensor_cfg_t cfg)
{
    _i2c_addr = cfg.i2c_addr;
    _ads_channel = cfg.ads_channel;
    _ads_sensor_unit = cfg.ads_sensor_unit;
    _input_low_val = cfg.input_low_val;
    _input_high_val = cfg.input_high_val;
    _output_low_val = cfg.output_low_val;
    _output_high_val = cfg.output_high_val;

    _p_ads = std::make_shared<Adafruit_ADS1115>();
}

ADS_Sensor::~ADS_Sensor() {}

bool ADS_Sensor::begin()
{
    return _p_ads->begin(_i2c_addr);
}

auto ADS_Sensor::getSensorUnitType() -> std::string
{
    return _ads_sensor_unit;
}
uint8_t ADS_Sensor::getSensorChannel()
{
    return _ads_channel;
}
auto ADS_Sensor::readADC() -> uint16_t
{
    return _p_ads->readADC_SingleEnded(_ads_channel);
}

auto ADS_Sensor::readVolts() -> float
{
    return _p_ads->computeVolts(_p_ads->readADC_SingleEnded(_ads_channel));
}

auto ADS_Sensor::readSensorUnits() -> float
{
    return (readVolts() - _input_low_val) / (_input_high_val - _input_low_val) * (_output_high_val - _output_low_val);
}