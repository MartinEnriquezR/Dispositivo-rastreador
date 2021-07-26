
import RPi.GPIO as GPIO
GPIO.setwarnings(False) # Ignorar las advertencias
GPIO.setmode(GPIO.BOARD) # Numeracion fisica de los pines
GPIO.setup(40, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Puerto 40 como entrada resistencia de Pull Down

while True:
    if GPIO.input(40) == GPIO.HIGH:
        print("Button was pushed!")