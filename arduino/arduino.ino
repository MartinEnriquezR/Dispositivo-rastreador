#include <SoftwareSerial.h>
SoftwareSerial SIM808(3,1); //Pin 3 Rx, Pin 1 Tx

void setup() {
  //tiempos para la comunicacion con el sim y el ajuste del puerto serie
  SIM808.begin(19200);
  Serial.begin(19200);
  delay(1000);
  Serial.println("Configuracion realizada");
}

void comandoAT(String comando, char* respuestaCorrecta){
    bool ejecutar = 0;
    char respuesta[100];
    memset(respuesta, '\0', 100); // Inicializa el string

    do{ 
        SIM808.read(); // se limpia el buffer de entrada
        SIM808.println(comando); // Envia el comando AT
        delay(100);

        if (SIM808.available() != 0){
            respuesta[x] = SIM808.read();   //se lee la respuesta que nos da el comando
            if ( strstr(respuesta, respuestaCorrecta) != NULL ){
                ejecutar = 1;
            }
        }

    }while(ejecutar == 0);

    Serial.println(respuesta);
    return ejecutar;
}

void loop() {
    Serial.println("Encender el GPS")
    comandoAT("AT","OK")
}