import smbus2
import bme280

# Setup
port = 1
address = 0x76
bus = smbus2.SMBus(port)
calibration_params = bme280.load_calibration_params(bus, address)


'''
The sample method will take a single reading and return a
compensated_reading object
    data = bme280.sample(bus, address, calibration_params)

The compensated_reading class has the following attributes
    attrs of data:
        data.id
        data.timestamp
        data.temperature
        data.pressure
        data.humidity
'''

def getBmeData() -> object:
    data: object = bme280.sample(bus, address, calibration_params)
    return(data)

def getTempAndHumidity() -> float:
    data: object        = bme280.sample(bus, address, calibration_params)
    temperature: float  = data.temperature * 9/5 + 32
    humidity: float     = data.humidity

    return(temperature, humidity)


def main() -> None:
    temperature, humidity = getTempAndHumidity()
    print(
        f"Temperature: {temperature:.2f}\n"
        f"Humidity[%]: {humidity:.2f}"
          )




if __name__== "__main__":
    main()