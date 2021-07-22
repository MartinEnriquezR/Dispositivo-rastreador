#librerias necesarias
import serial
import time
port = "/dev/ttyS0"

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
            print(str(respuesta))
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

ser = serial.Serial(port, baudrate = 9600, timeout = 0.5)
print('Encendiendo el modulo GPS')
encenderGPS()
time.sleep(5)
print('verificando el estado del GPS')
verificarStatusGPS()
print('obteniendo las coordenadas')

for i in range(5):
    latitud, longitud, timestamptz =obtenerCordenadas()
    print( str(timestamptz)+' '+str(latitud)+' '+str(longitud))
    time.sleep(20)

