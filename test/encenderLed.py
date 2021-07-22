#libreria de raspberry
import RPi.GPIO as GPIO

import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

puerto = 15

#configuracion de los pines de salida
GPIO.setup(puerto,GPIO.OUT)

#inicio
while True:
    print('Led encendido')
    GPIO.output(puerto,GPIO.HIGH)
    
    time.sleep(2)

    print('Led apagado')
    GPIO.output(puerto,GPIO.LOW)

    time.sleep(2)