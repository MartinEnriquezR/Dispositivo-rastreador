import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time


def button_callback(channel):
    #configurar el GPS
    #establecer la conexion AWS IoT
    #leer si existe un mensaje de salir de enviar la info 
    #crear el mensaje PAYLOAD 
    bucle = True
    while bucle == True:
        print('dentro de la interrupcion')
        bucle = False
        print('saliendo de la interrupcion' + str(bucle))


pin = 40
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #resistencia de pull down
GPIO.add_event_detect(pin,GPIO.RISING,callback=button_callback, bouncetime= 5000) # Setup event on pin 40 rising edge

while True:
    print('mensaje de prueba')
    time.sleep(4)