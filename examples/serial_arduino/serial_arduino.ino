/*
  Example Arduino sketch that can be used with serial_simple.py
*/

void setup() {
  Serial.begin(9600);
}

void loop() {
  Serial.write('a');
  delay(5000);
  Serial.write('b');
  delay(5000);
  Serial.write('a');
  delay(5000);
  Serial.write('b');
  delay(5000);
  for (char i = 0; i < 20; ++i) {
    Serial.write(i);
    delay(500);
  }
}
