#include <SoftwareSerial.h>
#include <IRremote.h>

int receiverpin=6;
long data;

decode_results results;

SoftwareSerial communication(10, 11);
IRrecv irrecv(receiverpin);
IRsend irsend;

byte buffer[2];

void setup() {
  Serial.begin(9600);
  communication.begin(9600);
  irrecv.enableIRIn();                                                                                                
}

long bufferToInt(byte* buffer) {
  long number = buffer[0];
  number = number << 8;
  number += buffer[1];
  return number;
}

void loop() {
  if(Serial.available()>0){
    Serial.readBytes(buffer, 2);
    data = bufferToInt(buffer);
    irsend.sendNEC(data, 32);
    delay(40);
    irsend.sendNEC(data, 32);
    delay(40);
    irsend.sendNEC(data, 32);
    delay(40);
    irrecv.enableIRIn();      
  }
  if(communication.available()>0) {
    Serial.println(communication.readString());
  }
  if (irrecv.decode(&results)) {
    Serial.println(results.value);
    irrecv.resume(); // Receive the next value
  }
}
