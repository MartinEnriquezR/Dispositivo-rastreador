
"""comandos para la configuracion
AT+CGATT=1 
#AT+CSTT="internet.itelcel.com"
#AT+CIICR
#AT+CIFSR
AT+SAPBR=3,1,"Contype","GPRS"-----------------------------------
AT+SAPBR=3,1,"APN","internet.itelcel.com"
AT+SAPBR=3,1,"USER","webgprs"
AT+SAPBR=3,1,"PWD","webgprs2002"
AT+SAPBR=1,1
AT+SAPBR=2,1----------------------------------------------------
"""

"""comandos para iniciar la comunicacion HTTP
AT+HTTPINIT
AT+HTTPPARA="CID",1
AT+HTTPPARA="URL","http://servidorpt2disp.us-east-1.elasticbeanstalk.com/"
AT+HTTPACTION=0
AT+HTTPREAD
AT+HTTPTERM
AT+SAPBR=0,1----------------------------------termina la comunicacion con el carrier
"""

import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time
import serial
import re

class GPRS:
    def __init__(self):
        time.sleep(10)
        print('1')
        self.enviarComando('AT+CGATT=1',r'OK',10)
        #print('2')
        #self.enviarComando('AT+CSTT=\"internet.itelcel.com\"',r'OK',10)
        #print('3')
        #self.enviarComando('AT+CIICR',r'OK',200)
        #print('4')
        #self.enviarComando('AT+CIFSR',r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',20)
        print('5')
        self.enviarComando('AT+SAPBR=3,1,\"Contype\",\"GPRS\"',r'OK',10)
        print('6')
        self.enviarComando('AT+SAPBR=3,1,\"APN\",\"internet.itelcel.com\"',r'OK',10)
        print('7')
        self.enviarComando('AT+SAPBR=3,1,\"USER\",\"webgprs\"',r'OK',10)
        print('8')
        self.enviarComando('AT+SAPBR=3,1,\"PWD\",\"webgprs2002\"',r'OK',10)
        print('9')
        self.enviarComando('AT+SAPBR=1,1',r'OK',10)
        print('10')
        self.enviarComando('AT+SAPBR=2,1',r'+SAPBR:\s1,1',10)

    def enviarComando(self, comando, patron, tiempo):
        
        ejecutar = True

        while ejecutar == True:

            conteoRespuestas = 0
            respuestasRecibidas = ''
        
            ser.write(bytes("{}\r".format(comando),encoding='utf-8'))    
            while conteoRespuestas < tiempo:
                respuesta = ser.readline()
                print(respuesta)
                respuestasRecibidas += respuesta.decode('utf-8')
                conteoRespuestas += 1
                
            if re.search(patron,respuestasRecibidas):
                #Se encontro la respuesta
                print('------------' + respuestasRecibidas)
                ejecutar = False
            
"""

def leerRespuesta():
    comando = 'AT+HTTPREAD'
    respuesta = ''
    ejecutar = True
    while ejecutar == True:
        esperarRespuesta = 0
        ser.write(b'{}\r'.format(comando))
        
        while esperarRespuesta <20:
            respuesta += ser.readline()
            esperarRespuesta += 1

        #buscar el inicio COMANDO
        
        #buscar el final OK
        
        #leer en medio

def configurarHTTP():

def comunicacionHTTP(String url, String accion ):
    #configuracion
    enviarComando('AT+HTTPINIT')
    enviarComando('AT+HTTPPARA=\"CID\",1')
    enviarComando('AT+HTTPPARA="URL","{}"'.format(pagina))
    
    ejecutar = True
    while ejecutar == True:
        esperarRespuesta = 0
        ser.write(b'AT+HTTPACTION=0\r')
        time.sleep(10000)
        while esperarRespuesta <10:
            respuesta = ser.readline()
            decodeData = respuesta.decode('utf-8')        
            if decodeData[0:18] == "+HTTPACTION: 0,200":
                #salir de la ejecucion
                ejecutar = False
                break
            elif: decodeData[0:18] == "+HTTPACTION: 0,201":
                #salir de la ejecucion
                ejecutar = False
                break
            elif: decodeData[0:18] == "+HTTPACTION: 0,202":
                #salir de la ejecucion
                ejecutar = False
                break 
            esperarRespuesta += 1
    
    


    enviarComando('AT+HTTPTERM')
    enviarComando('AT+SAPBR=0,1')
"""


#configuracion del puerto
port = "/dev/ttyS0"
ser = serial.Serial(port, baudrate = 9600, timeout = 0.5)

#inicio del programa
SIM808GPRS = GPRS()

