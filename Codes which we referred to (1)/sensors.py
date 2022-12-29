import wiringpi as wiringpi
from time import sleep
import RPi.GPIO as GPIO
import time

wiringpi.wiringPiSetupGpio()
wiringpi.pinMode(18, 0)
count=0

my_input=wiringpi.digitalRead(25)
if(my_input):
	print("Not Detected !")
else:
	print("Alcohol Detected")
	
sleep(1)


sensor = 33
buzzer = 18

GPIO.setmode(GPIO.BOARD)
GPIO.setup(sensor,GPIO.IN)
GPIO.setup(buzzer,GPIO.OUT)

GPIO.output(buzzer,False)
print ("IR Sensor Ready.....")
print (" ")


while True:
      if GPIO.input(sensor):
          GPIO.output(buzzer,True)
          print ("Object Detected")
          while GPIO.input(sensor):
              time.sleep(0.2)
      else:
          GPIO.output(buzzer,False)
          print("Object not detected")







 
#GPIO SETUP
channel = 35
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)
 
def callback(channel):
        if GPIO.input(channel):
                print ("Movement Detected!")
        else:
                print ("Movement Detected!")
 
GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300)  # let us know when the pin goes HIGH or LOW
GPIO.add_event_callback(channel, callback)  # assign function to GPIO PIN, Run function on change
 
# infinite loop
while True:
        time.sleep(1)