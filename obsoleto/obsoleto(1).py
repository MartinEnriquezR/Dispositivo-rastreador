#librerias de aws iot 
# Import SDK packages
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient



def customCallback(payload, responseStatus, token):
    if responseStatus == 'timeout':
        print(responseStatus)
        print(token)
        print('timeout')
    if responseStatus == 'accepted':
        print('accepted')
        print(token)
        print(payload)
    if responseStatus == 'rejected':
        print('rejected')


#Inicio del programa 
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


# Iniciar la conexion
myShadowClient = AWSIoTMQTTShadowClient(clientId)
myShadowClient.configureEndpoint(endpoint, 8883)
myShadowClient.configureCredentials(rootCA,privateKey,cert)

# AWSIoTMQTTShadowClient configuracion de la conexion 
#Funciones que se deben de llamar antes de establecer la conexion 
myShadowClient.configureAutoReconnectBackoffTime(1, 32, 20)    #la reconexion inicia en un segundo tiempo maximo de reconexion 32 seg, la conexion cada 20 segundos es estable
myShadowClient.configureConnectDisconnectTimeout(10) # 10 sec  #tiempo para esperar el mensaje CONNACK o dar la conectividad por perdida
myShadowClient.configureMQTTOperationTimeout(5) # 5 sec #se usa para definir el timeout del QoS 1 


#conectarme por medio de AWS Shadow
myShadowClient.connect()
#manejador de la conexion
myDeviceShadow = myShadowClient.createShadowHandlerWithName(thingName,True)

# Shadow operations
#myDeviceShadow.shadowGet(customCallback, 5)
#myShadowClient.disconnect()
#myDeviceShadow.shadowUpdate(myJSONPayload, customCallback, 5)
#myDeviceShadow.shadowDelete(customCallback, 5)
#myDeviceShadow.shadowRegisterDeltaCallback(customCallback)
#myDeviceShadow.shadowUnregisterDeltaCallback()

#conexion normal de MQTT
#myMQTTClient = myShadowClient.getMQTTConnection()
#myMQTTClient.publish(topicoEnviar, "Payload", 1) 


