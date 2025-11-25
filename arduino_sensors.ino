#include <Wire.h>

#define I2C_ADDRESS 0x08

// Sensor pins
#define PIN_V_PV    A0
#define PIN_V_WIND  A1
#define PIN_I_PV    A2
#define PIN_I_WIND  A3

// Calibration (modify to match your sensors)
float Vref = 5.0;
float ADC_max = 1023.0;

// Example sensor conversions
float voltageDividerRatio = 11.0; // for standard 30V sensor
float acs_sensitivity = 0.066;    // ACS712 30A = 66mV/A
float acs_zero = 2.5;             // Midpoint reading

// Data packet (4 floats)
float pv_voltage = 0, wind_voltage = 0;
float pv_current = 0, wind_current = 0;

void requestEvent() {
  Wire.write((byte*) &pv_voltage, 4);
  Wire.write((byte*) &wind_voltage, 4);
  Wire.write((byte*) &pv_current, 4);
  Wire.write((byte*) &wind_current, 4);
}

void setup() {
  Serial.begin(115200);
  Wire.begin(I2C_ADDRESS);

  Serial.println("I2C Power Sensor Node Started!");
}

void loop() {

  // ----- READ SENSORS -----
  int raw_pv_v = analogRead(PIN_V_PV);
  int raw_wind_v = analogRead(PIN_V_WIND);
  int raw_pv_i = analogRead(PIN_I_PV);
  int raw_wind_i = analogRead(PIN_I_WIND);

  // ----- CONVERSIONS -----
  float pv_v_adc = (raw_pv_v * Vref) / ADC_max;
  float wind_v_adc = (raw_wind_v * Vref) / ADC_max;

  pv_voltage = pv_v_adc * voltageDividerRatio;
  wind_voltage = wind_v_adc * voltageDividerRatio;

  float pv_i_voltage = (raw_pv_i * Vref) / ADC_max;
  float wind_i_voltage = (raw_wind_i * Vref) / ADC_max;

  pv_current = (pv_i_voltage - acs_zero) / acs_sensitivity;
  wind_current = (wind_i_voltage - acs_zero) / acs_sensitivity;

  // ----- SERIAL DEBUG -----
  Serial.println("========= SENSOR DATA =========");
  Serial.print("PV Voltage Raw: "); Serial.println(raw_pv_v);
  Serial.print("Wind Voltage Raw: "); Serial.println(raw_wind_v);
  Serial.print("PV Current Raw: "); Serial.println(raw_pv_i);
  Serial.print("Wind Current Raw: "); Serial.println(raw_wind_i);

  Serial.print("PV Voltage (V): "); Serial.println(pv_voltage);
  Serial.print("Wind Voltage (V): "); Serial.println(wind_voltage);
  Serial.print("PV Current (A): "); Serial.println(pv_current);
  Serial.print("Wind Current (A): "); Serial.println(wind_current);
  Serial.println("================================\n");

  delay(300);
}
