#include <SoftwareSerial.h>
// 7 - Rx, 8 - Tx
SoftwareSerial SIM808(7,8);

void setup(){
    SIM808.begin(9600);
    Serial.begin(9600);
    delay(100);
}

void loop(){
    //Envíamos y recibimos datos
    if (Serial.available() > 0)
        SIM808.write(Serial.read());
    if (SIM808.available() > 0)
        Serial.write(SIM808.read());
}