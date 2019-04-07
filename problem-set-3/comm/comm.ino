#include <SoftwareSerial.h>

String incomingStr = "";   // for incoming serial string data

// 10 -> RX, 11 -> TX
SoftwareSerial communication(10, 11);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  communication.begin(9600);
}


void loop() {
  if (communication.available() > 0) {
    incomingStr = communication.readString();
    Serial.println(incomingStr);
  }

  if(Serial.available() > 0) {
    incomingStr = Serial.readString();
    communication.println(incomingStr);
  }
}
