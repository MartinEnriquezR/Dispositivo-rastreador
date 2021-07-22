#include <SoftwareSerial.h>

//configuracion de los pines
SoftwareSerial SIM808(2,3);
//configurar la velocidad de la comunicacion serial
void setup(){
    SIM808.begin(9600);
    Serial.begin(9600);
    delay(1000);
    //encender el GPS
    encenderGPS();
    Serial.println("Configuracion realizada y modulo GPS encendido");
}
//funcion para el envio de comandos AT
int enviarAT(String comando, char* respuestaCorrecta, unsigned int tiempo){
    //declaracion de variables
    int indice = 0;
    bool correcto = 0;
    char respuesta[100];
    unsigned long anterior;

    memset(respuesta, '\0', 100); // Inicializa el string
    delay(100);
    while( SIM808.available() > 0) SIM808.read();   // Limpia el buffer de entrada
    
    SIM808.println(comando); // Envia el comando AT
    indice = 0;
    anterior = millis();
    
    do{
        if (SIM808.available() != 0){
            respuesta[indice] = SIM808.read();
            indice++;
            if ( strstr(respuesta, respuestaCorrecta) != NULL){
                correcto = 1;
            }
        }
    } while( (correcto == 0) && ( (millis() - anterior) < tiempo ));
  
    return correcto;
}
//funcion para encender el modulo GPS
void encenderGPS(){
    //comando at AT+CGPSPWR=1
    int ejecutar = 0;
    do{
        ejecutar = enviarAT("AT+CGPSPWR=1","OK",5000);
    }while (ejecutar == 0);
}
//funcion para verificar el estado del modulo GPS
void verificarStatus(){
    //comando AT AT+CGPSSTATUS?
    int ejecutar = 0;
    do{
        ejecutar = enviarAT("AT+CGPSSTATUS?","+CGPSSTATUS: Location 3D Fix","5000");
    }while( ejecutar == 0);
    
}
//funcion para obtener las cordenadas geograficas
void obtenerCordenadas(){

    //declaracion de variables
    String comando = "AT+CGNSINF";
    int indice = 0;
    bool correcto = 0;
    char respuesta[100];
    memset(respuesta, '\0', 100); // Inicializa el string
    delay(100);
    
    Serial.println("Dentro de la funcion");
    verificarStatus();
    Serial.println("Estado verificado");

    while( SIM808.available() > 0) SIM808.read();   // Limpia el buffer de entrada
    
    SIM808.println(comando); // Envia el comando AT
    indice = 0;
    do{
        if (SIM808.available() != 0){
            respuesta[indice] = SIM808.read();
            indice++;
            Serial.println(respuesta);
            Serial.println(indice);
            if (indice == 70){
                correcto = 1;
            }
        }
    } while( correcto == 0 );
    Serial.println("-----------");
    Serial.println(respuesta);
    Serial.println("-----------");

}

void loop(){
    //String payload[3];
    obtenerCordenadas();
    delay(10000);
    //obtenercordenadas(cordenadas);
    //Serial.println(cordenadas[0]);
    //Serial.println(cordenadas[1]);
    //Serial.println(cordenadas[2]);
}

