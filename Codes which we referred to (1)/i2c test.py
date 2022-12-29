from signal import signal, SIGTERM, SIGHUP, pause
from rpi_lcd import LCD
import RPi.GPIO as GPIO

ir = 33
vibration  = 35
smoke = 18

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)



lcd = LCD()
def safe_exit(signum, frame):
    exit(1)
try:
    signal(SIGTERM, safe_exit)
    signal(SIGHUP, safe_exit)
    lcd.text("Hello", 1)
    lcd.text("IPR 18!", 2)
    pause()
    '''if GPIO.input(ir):
        lcd.text("test")'''
except KeyboardInterrupt:
    pass
finally:
    lcd.clear()