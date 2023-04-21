#include <Wire.h>
#include "Adafruit_MPRLS.h"

// You dont *need* a reset and EOC pin for most uses, so we set to -1 and don't connect
#define RESET_PIN  -1  // set to any GPIO pin # to hard-reset on begin()
#define EOC_PIN    -1  // set to any GPIO pin to read end-of-conversion by pin
Adafruit_MPRLS mpr = Adafruit_MPRLS(RESET_PIN, EOC_PIN);
float p_zero;

void setup() {
  Serial.begin(115200);
  Serial.println("MPRLS Simple Test");
  if (! mpr.begin()) {
    Serial.println("Failed to communicate with MPRLS sensor, check wiring?");
    while (1) {
      delay(10);
    }
  }
  Serial.println("Found MPRLS sensor");
  p_zero = mpr.readPressure();
}


void loop() {
  float pressure_hPa = mpr.readPressure() - p_zero;
//  Serial.print("Pressure (hPa): "); Serial.println(pressure_hPa);
  Serial.print("P:"); Serial.println(pressure_hPa / 68.947572932);
  delay(1);
}
