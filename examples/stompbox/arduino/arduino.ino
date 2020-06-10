void setup() {
  // put your setup code here, to run once:
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(2, INPUT_PULLUP);
  digitalWrite(LED_BUILTIN, HIGH);
  Serial.begin(9600);
}

bool prevState = HIGH;

void loop() {
  // put your main code here, to run repeatedly:
  bool state = digitalRead(2);
  if (state != prevState) {
    if (state) {
      Serial.print("u");
    } else {
      Serial.print("d");
    }
    prevState = state;
    delay(30);
  }
}
