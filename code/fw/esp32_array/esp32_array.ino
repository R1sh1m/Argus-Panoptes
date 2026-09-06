// Argus-Panoptes ESP32 array firmware
// Mode0 sequential cal, Mode1 flood (1Tx + 4Rx), Mode2 phased focus.
// Wire: Trig ESP32 GPIO direct, Echo 5V -> 1k/2k divider -> 3.3V GPIO. Common GND.
//
// Pins: TRIG = {25, 26, 27, 14}, ECHO = {34, 35, 32, 33} (input-only 34+ safe)
// Positions_mm = {0, 41, 85, 130}
// Usage: Serial 115200, commands: CAL, FLOOD, FOCUS Xf_mm Zf_mm, ROCK
// Output CSV: t,T_C,d[4],peak[4],width[4]

#include <Arduino.h>

const int N = 4;
const int TRIG[N] = {25, 26, 27, 14};
const int ECHO[N] = {34, 35, 32, 33};
const float POS[N] = {0, 41, 85, 130};
const float SOUND_BASE = 331.4;

float readTempC() { return 25.0; }  // TODO: DS18B20
float soundSpeed(float T) { return SOUND_BASE + 0.6f * T; }

long pingOnce(int i, float c, long timeout_us = 30000) {
  digitalWrite(TRIG[i], LOW); delayMicroseconds(2);
  digitalWrite(TRIG[i], HIGH); delayMicroseconds(10);
  digitalWrite(TRIG[i], LOW);
  long us = pulseIn(ECHO[i], HIGH, timeout_us);
  return us;
}

void setup() {
  Serial.begin(115200);
  for (int i = 0; i < N; i++) {
    pinMode(TRIG[i], OUTPUT); digitalWrite(TRIG[i], LOW);
    pinMode(ECHO[i], INPUT);
  }
  Serial.println("# Argus ESP32 ready. CMD: CAL FLOOD FOCUS Xf Zf");
}

void doCalFlood(bool floodOnlyTx0) {
  float T = readTempC(), c = soundSpeed(T);
  long t = millis();
  Serial.print("T,"); Serial.print(t); Serial.print(",C,"); Serial.print(T);
  for (int i = 0; i < N; i++) {
    int tx = floodOnlyTx0 ? 0 : i;
    // In flood mode Tx0 fires, all Rx listen; here simplified sequential.
    // TODO: RMT phased delays + pin-change ISR parallel capture.
    digitalWrite(TRIG[tx], LOW); delayMicroseconds(2);
    digitalWrite(TRIG[tx], HIGH); delayMicroseconds(10);
    digitalWrite(TRIG[tx], LOW);
    long us = pulseIn(ECHO[i], HIGH, 30000);
    float dmm = us * c / 2000.0f;
    Serial.print(",d"); Serial.print(i); Serial.print(","); Serial.print(dmm, 1);
    Serial.print(",us"); Serial.print(i); Serial.print(","); Serial.print(us);
    delay(60);  // guard vs crosstalk
  }
  Serial.println();
}

void doFocus(float Xf, float Zf, float T) {
  float c = soundSpeed(T);  // mm/ms
  float cmm_us = c * 1000.0f / 1e6f;  // mm per us
  float dist[N], mx = 0;
  for (int i = 0; i < N; i++) {
    float dx = POS[i] - Xf;
    dist[i] = sqrt(dx * dx + Zf * Zf);
    if (dist[i] > mx) mx = dist[i];
  }
  Serial.print("# FOCUS Xf="); Serial.print(Xf);
  Serial.print(" Zf="); Serial.print(Zf);
  for (int i = 0; i < N; i++) {
    float delay_us = (mx - dist[i]) / cmm_us;
    Serial.print(" d"); Serial.print(i); Serial.print("="); Serial.print(delay_us, 1);
  }
  Serial.println("us (outer-first = converging)");
  // TODO: RMT fire TRIG[i] with delay_us offsets, then parallel capture.
}

void loop() {
  if (Serial.available()) {
    String s = Serial.readStringUntil('\n'); s.trim();
    if (s == "CAL") doCalFlood(false);
    else if (s == "FLOOD") doCalFlood(true);
    else if (s.startsWith("FOCUS")) {
      float Xf = 65, Zf = 300;
      sscanf(s.c_str(), "FOCUS %f %f", &Xf, &Zf);
      doFocus(Xf, Zf, readTempC());
    }
    else Serial.println("# CMD: CAL FLOOD FOCUS Xf_mm Zf_mm");
  }
}
