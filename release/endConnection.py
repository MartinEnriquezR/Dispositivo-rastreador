import RPi.GPIO as GPIO #librerias de Raspberry Pi GPIO
import serial, time, re #librerias de python
port = "/dev/ttyS0" #direccion del puerto serial

class SIM808:
    
    """funcion para enviar comandos AT"""
    def comando(self,comando,patron,tiempo):
        ejecucion = True
        while ejecucion == True:
            
            conteoRespuestas = 0
            respuestasRecibidas = ''
            mensaje = bytes('{}\r'.format(comando),encoding='utf-8')
            print('Comando: {} ingresado'.format(mensaje))
            ser.write(mensaje)

            while conteoRespuestas < tiempo:
                respuesta = ser.readline()
                respuestasRecibidas += respuesta.decode('utf-8')
                conteoRespuestas += 1

            if re.search(patron,respuestasRecibidas):
                ejecucion = False
    
    """inicializar el sim808"""
    def __init__(self):
        pass
    
    #funcion para cerrar la conexion 
    def finalizarConexionHTTP(self):
        print('---Finalizando conexion HTTP---')

        self.comando('AT+HTTPTERM',r'OK',10) #terminate http service
        self.comando('AT+SAPBR=0,1',r'OK',10) #cerrando la comunicacion GPRS

        print('---Conexion HTTP finalizada---')


"""Configurando la tarjeta"""
ser = serial.Serial(port,baudrate=9600,timeout=0.5) #configuracion del puerto serial
modulo = SIM808() #inicializar el SIM808
"""Enviando una alerta"""
modulo.finalizarConexionHTTP()