#define USE_ARDUINO_INTERRUPTS true
#include <PulseSensorPlayground.h>

String receivedData;

const int PulseWire = A0;       // Connect the PulseSensor to ANALOG PIN A0
int Threshold = 550;

PulseSensorPlayground pulseSensor;

void setup() {
  pinMode(13, OUTPUT);
  pinMode(8, OUTPUT);

  Serial.begin(9600);
  Serial.setTimeout(10);

 // pulseSensor.analogInput(PulseWire);
  pulseSensor.setThreshold(Threshold);

  if (pulseSensor.begin()) {
//    Serial.println("PulseSensor object created!");
  }
}

void loop() {
  if (Serial.available() > 0) {
    receivedData = Serial.readStringUntil('\n');

    if (receivedData == "Having Diabetes") {
      digitalWrite(8, HIGH); 
      delay(1000);
      digitalWrite(8, LOW);}
    // } else if (receivedData == "Hypertension Stage 2") {
    //   digitalWrite(8, HIGH); 
    //   delay(2000);
    //   digitalWrite(8, LOW);
    // }
  }

// int value =analogRead(PulseWire);
// Serial.println(value);
  if (pulseSensor.sawStartOfBeat()) {
    int myBPM = pulseSensor.getBeatsPerMinute();
//    Serial.print("BPM: ");
    Serial.println(myBPM);
  }

  delay(20);
}