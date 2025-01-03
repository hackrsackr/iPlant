import smbus2
import bme280

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

def getBmeData(addr: str, bus: object, params: object) -> object:
    data: object = bme280.sample(bus, addr, params)

    return(data)

def getTempAndHumidity(addr: str, bus: object, params: object) -> float:
    data: object        = bme280.sample(bus, addr, params)
    temperature: float  = data.temperature * 9/5 + 32
    humidity: float     = data.humidity

    return(temperature, humidity)

def main() -> None:
    port: int = 1
    address: str = 0x76
    bus: object = smbus2.SMBus(port)
    calibration_params: object = bme280.load_calibration_params(bus, address)
    
    temperature, humidity = getTempAndHumidity(addr=address, bus=bus, params=calibration_params)
    
    print(
        f"Temperature: {temperature:.2f}\n"
        f"Humidity[%]: {humidity:.2f}"
          )

if __name__== "__main__":
    main()