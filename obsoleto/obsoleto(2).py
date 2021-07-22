from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time
import serial
import json

#variables de funcionamiento
numeroSerie = 1
#credenciales necesarias para el  funcionamiento 
endpoint = 'a34fft2urvu4gr-ats.iot.us-east-1.amazonaws.com'
rootCA = 'certs/Amazon-root-CA-1.pem'
cert = 'certs/device.pem.crt'
privateKey = 'certs/private.pem.key'
port = 8883                         #puerto de MQTT
thingName = 'dispositivo'
clientId = 'dispositivo'
topicoEnviar = 'topicoPrueba'
port = "/dev/ttyS0"
pin = 40

def encenderGPS():
    ejecutar = True
    while ejecutar == True:
        esperarRespuesta = 0
        ser.write(b'AT+CGPSPWR=1\r')
        while esperarRespuesta <10:
            respuesta = ser.readline()
            if respuesta == b'OK\r\n':
                ejecutar = False
                break
            esperarRespuesta += 1

def verificarStatusGPS():
    ejecutar = True
    while ejecutar == True:
        esperarRespuesta = 0
        ser.write(b'AT+CGPSSTATUS?\r')
        time.sleep(0.1)
        while esperarRespuesta < 10:
            respuesta = ser.readline()
            #print(str(respuesta))
            time.sleep(0.1)
            if respuesta == b'+CGPSSTATUS: Location 3D Fix\r\n': # or respuesta == b'+CGPSSTATUS: Location 2D Fix\r\n':
                ejecutar = False
                break
            esperarRespuesta += 1

def obtenerCordenadas():
    ejecutar = True
    while ejecutar == True:
        esperarRespuesta = 0    
        ser.write(b'AT+CGNSINF\r')
        while esperarRespuesta < 10:
            respuesta = ser.readline()
            decodeData = respuesta.decode('utf-8')        
            if decodeData[0:8] == "+CGNSINF":
                decodeData = decodeData.split(",")
                timestamptz = decodeData[2][0:4]+"-"+decodeData[2][4:6]+"-"+decodeData[2][6:8]+" "+decodeData[2][8:10]+":"+decodeData[2][10:12]+":"+decodeData[2][12:14]+"-"+"06"
                latitud= decodeData[3]
                longitud= decodeData[4]
                #salir de la ejecucion
                ejecutar = False
                break
            else:
                esperarRespuesta += 1
    return latitud, longitud, timestamptz

def interrupcion(channel):
    
    #conectarme por medio de AWS Shadow
    myShadowClient.connect()
    #manejador de la conexion
    myDeviceShadow = myShadowClient.createShadowHandlerWithName(thingName,True)
    #conexion normal de MQTT
    myMQTTClient = myShadowClient.getMQTTConnection()
        
    ejecutar = True
    while ejecutar == True:
        print('verificando ...')
        verificarStatusGPS()
        print('estado verificado')
        latitud, longitud, timestamptz =obtenerCordenadas()
        print( str(timestamptz)+' '+str(latitud)+' '+str(longitud))
        
        # Create el mensaje que se va a reportar  
        print('Creando mensaje ...')
        payload = {
            "state":{
                "reported":{
                    "numeroSerie": str(numeroSerie),
                    "latitud": str(latitud),
                    "longitud": str(longitud),
                    "timestamptz": str(timestamptz)
                    }
            }
        }
        myMQTTClient.publish(topicoEnviar,json.dumps(payload),1) 
        time.sleep(5)

def configurarConexion():
    myShadowClient.configureEndpoint(endpoint, 8883)
    myShadowClient.configureCredentials(rootCA,privateKey,cert)
    # AWSIoTMQTTShadowClient configuracion de la conexion 
    #Funciones que se deben de llamar antes de establecer la conexion 
    myShadowClient.configureAutoReconnectBackoffTime(1, 32, 20)    #la reconexion inicia en un segundo tiempo maximo de reconexion 32 seg, la conexion cada 20 segundos es estable
    myShadowClient.configureConnectDisconnectTimeout(10) # 10 sec  #tiempo para esperar el mensaje CONNACK o dar la conectividad por perdida
    myShadowClient.configureMQTTOperationTimeout(5) # 5 sec #se usa para definir el timeout del QoS 1 

#Inicio del programa 
#Configuracion del la comunicacion serial
ser = serial.Serial(port, baudrate = 9600, timeout = 0.5)
#Configurando el pin de interrupcion
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #resistencia de pull down
GPIO.add_event_detect(pin,GPIO.RISING,callback=interrupcion, bouncetime= 5000) # Setup event on pin 40 rising edge
# Iniciar la conexion
myShadowClient = AWSIoTMQTTShadowClient(clientId)
configurarConexion()
#Inicio del programa
encenderGPS()
time.sleep(5)
while True:
    print('Dispositivo en espera de interrupcion')
    time.sleep(1)
    