import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(19, GPIO.IN) 
ledstate = 0
try:
    while True:
        if GPIO.input(19) == 0 and ledstate == 0:
            print ("led is On")
            GPIO.output (18, True)
            ledstate = 1
            time.sleep (0.5)
        if GPIO.input (19) == 1 and ledstate == 1:
            print ("led is OFF")
            GPIO.output (18, False)
            ledstate =0
            time.sleep(0.5)
finally:
  GPIO.cleanup ()