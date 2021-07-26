import RPi.GPIO as GPIO
import time


def alerta(channel):
    print('dentro de la interrupcion')
    print('saliendo de la interrupcion')


push_button = 40 # pin del boton
GPIO.setwarnings(False) #apagar los warnings
GPIO.setmode(GPIO.BOARD) #numeracion de la placa
GPIO.setup( # entrada con resistencia pull-down
    push_button, 
    GPIO.IN, 
    pull_up_down=GPIO.PUD_DOWN
)
GPIO.add_event_detect( #configuracion de la interrupcion
    push_button,
    GPIO.RISING,
    callback=alerta, 
    bouncetime= 3000
)

while True: #bucle infinito
    print('mensaje de prueba')
    time.sleep(1)