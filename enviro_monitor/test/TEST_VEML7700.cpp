#include "Arduino.h"
#include "Adafruit_VEML7700.h"

Adafruit_VEML7700 veml = Adafruit_VEML7700();
constexpr auto I2C_SCL(17);
constexpr auto I2C_SDA(18);

void printValues() 
{ 
    Serial.printf("ALS: %2.2f \n", veml.readALS());
    Serial.printf("Raw White: %2.2f \n", veml.readWhite());
    Serial.printf("Raw Lux: %2.2f \n", veml.readLux());
    Serial.printf("Auto Lux: %2.2f \n", veml.readLux(VEML_LUX_AUTO));
    Serial.println();
}

void checkInterruptStatus() {
    uint16_t irq = veml.interruptStatus();
    if (irq & VEML7700_INTERRUPT_LOW) {
        Serial.println("** Low threshold");
    }
    if (irq & VEML7700_INTERRUPT_HIGH) {
        Serial.println("** High threshold");
    }
}

void setup() {
  Serial.begin(115200);
  while (!Serial) { delay(10); }
  Serial.println("Adafruit VEML7700 Test");
  
  Wire.begin(I2C_SDA, I2C_SCL);

  if (!veml.begin()) {
    Serial.println("Sensor not found");
    while (1);
  }
  Serial.println("Sensor found");
  
  veml.setLowThreshold(10000);
  veml.setHighThreshold(20000);
  veml.interruptEnable(true);

  // == OPTIONAL =====
  // Can set non-default gain and integration time to
  // adjust for different lighting conditions.
  // =================
  veml.setGain(VEML7700_GAIN_1_8);
  veml.setIntegrationTime(VEML7700_IT_50MS);

//   Serial.print(F("Gain: "));
//   switch (veml.getGain()) {
//     case VEML7700_GAIN_1: Serial.println("1"); break;
//     case VEML7700_GAIN_2: Serial.println("2"); break;
//     case VEML7700_GAIN_1_4: Serial.println("1/4"); break;
//     case VEML7700_GAIN_1_8: Serial.println("1/8"); break;
//   }

//   Serial.print(F("Integration Time (ms): "));
//   switch (veml.getIntegrationTime()) {
//     case VEML7700_IT_25MS: Serial.println("25"); break;
//     case VEML7700_IT_50MS: Serial.println("50"); break;
//     case VEML7700_IT_100MS: Serial.println("100"); break;
//     case VEML7700_IT_200MS: Serial.println("200"); break;
//     case VEML7700_IT_400MS: Serial.println("400"); break;
//     case VEML7700_IT_800MS: Serial.println("800"); break;
//   }

}

void loop() {
    veml.computeLux()
    printValues();
    checkInterruptStatus();
    delay(1000);
}

