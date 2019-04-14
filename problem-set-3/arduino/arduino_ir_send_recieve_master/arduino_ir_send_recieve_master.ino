#include <SoftwareSerial.h>
#include <IRremote.h>

int receiverpin=5;

String IV,msg;
char* temp;
long msgNum;
bool IVUnset=true;
char temp2[9];
long data;

decode_results results;

SoftwareSerial communication(10, 11);
IRrecv irrecv(receiverpin);
IRsend irsend;

byte buffer[2];

long bufferToInt(byte* buffer) {
  long number = buffer[0];
  number = number << 8;
  number += buffer[1];
  return number;
}

void setup() {
  Serial.begin(9600);
  communication.begin(9600);
  while(IVUnset){
    if (Serial.available()>0) {
      IV=Serial.readString();
      IVUnset=false;
      if(IV.length()==65){
        for(int i=0;i<64;i++){
          if(IV[i]!='0' && IV[i]!='1'){
             Serial.println("Wrong char");
             IVUnset=true;
             break;
          }
        }
      }else{
        Serial.println("Wrong len");
        IVUnset=true;
      }
    }
  }
  irrecv.enableIRIn();
  communication.print(IV);
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
  if(communication.available()>0){
    Serial.println(communication.readString());
  }
  if (irrecv.decode(&results)) {
    Serial.println(results.value, BIN);
    irrecv.resume();
  }
}
