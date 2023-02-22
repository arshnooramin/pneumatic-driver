#include <Wire.h>
#include <Adafruit_MPRLS.h>

#define RESET_PIN  -1
#define EOC_PIN    -1
#define CONV_FACTOR 68.947572932

Adafruit_MPRLS mpr = Adafruit_MPRLS(RESET_PIN, EOC_PIN);
float p_zero;
char rcv;

boolean start = false;

int relay1 = 4;
int relay2 = 5;
int relay3 = 6;
int relay4 = 7;

void updateZero() {
  p_zero = mpr.readPressure();
}

void setup() {
  
  Serial.begin(9600);
  if (!mpr.begin()) {
    Serial.println("ERROR: MRPLS Not Found.");
    while (1) delay(10);
  }
  
  Serial.println("SUCCESS: MRPLS Found.");
  
  updateZero();
  pinMode(relay1, OUTPUT);
  pinMode(relay2, OUTPUT);
  pinMode(relay3, OUTPUT);
  pinMode(relay4, OUTPUT);

  digitalWrite(relay1, LOW);
  digitalWrite(relay2, LOW);
  digitalWrite(relay3, LOW);
  digitalWrite(relay4, LOW);
}

void loop() {
  if (Serial.available() > 0) {
    rcv = Serial.read();
    if (rcv == '1') {
      digitalWrite(relay1, HIGH);
    } 
    if (rcv == '6') {
      digitalWrite(relay1, LOW);
    }
    if (rcv == '2') {
      digitalWrite(relay2, HIGH);
    }
    if (rcv == '7') {
      digitalWrite(relay2, LOW);
    }
    if (rcv == '3') {
      digitalWrite(relay3, HIGH);
    }
    if (rcv == '8') {
      digitalWrite(relay3, LOW);
    }
    if (rcv == '4') {
      digitalWrite(relay4, HIGH);
    }
    if (rcv == '9') {
      digitalWrite(relay4, LOW);
    }
  }
  
  float p_hPa = mpr.readPressure();
  Serial.print("p_val:"); Serial.println((p_hPa - p_zero)/CONV_FACTOR);
  delay(1000);
}
