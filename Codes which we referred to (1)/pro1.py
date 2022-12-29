import wiringpi as wiringpi
from time import sleep
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
import pynmea2
import serial

import string
from signal import signal, SIGTERM, SIGHUP, pause
ser=serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=1)
wiringpi.wiringPiSetupGpio()
wiringpi.pinMode(18, 0)
sensor = 33
relay = 36
Buzzer = 29
switch= 22
vibration=35
red_led=31
green_led=32
GPIO.setup(Buzzer, GPIO.OUT)
GPIO.setup(switch, GPIO.IN)
GPIO.setup(red_led, GPIO.OUT)
GPIO.setup(green_led, GPIO.OUT)
GPIO.setup(relay , GPIO.OUT)
GPIO.setup(vibration, GPIO.IN)
GPIO.setup(sensor,GPIO.IN)
print("Welcome\nAlcohol Detection System")

GPIO.output(Buzzer, False)
GPIO.output(green_led, False)
GPIO.output(red_led, True)
GPIO.output(relay,GPIO.HIGH)
while 1:
                car_start=0
                my_input=wiringpi.digitalRead(25)
                #car_start =0
                if (GPIO.input(sensor)==False):
                          GPIO.output(Buzzer,True)
                          print ("Seat belt worn")
                          #while GPIO.input(vibration):
                          time.sleep(0.2)
                          if (my_input==True):
                              print(" Alcohol Not Detected !")
                              GPIO.output(Buzzer, False)
                              GPIO.output(green_led, True)
                              GPIO.output(red_led, False)
                              time.sleep(0.5)
                          
                              while (1):
                                    if(car_start == 0):
                                        print("press the switch")
                                        time.sleep(0.5)
                                        switch_data= GPIO.input(switch)
                                    vibration_data =  GPIO.input(vibration)
                                    if(vibration_data==GPIO.HIGH):
                                            print("Accident Detected")
                                            GPIO.output(relay, GPIO.LOW)
                                            time.sleep(2)
                                            dataout =pynmea2.NMEAStreamReader()
                                           # serial=ser
                                            newdata=ser.readline()
                                            if '$GPRMC' in str(newdata):
                                                print(newdata.decode('utf-8'))
                                                newmsg=pynmea2.parse(newdata.decode('utf-8'))  
                                                lat=newmsg.latitude 
                                                lng=newmsg.longitude 
                                                gps = "Latitude=" + str(lat) + "and Longitude=" +str(lng)
                                                print(gps)
                                                time.sleep(2)
                                            break
                                            
                                            
                                    elif(switch_data == 1):
                                             print("vehicle start ")
                                             GPIO.output(red_led, False)
                                             GPIO.output(relay,True)
                                             car_start = 1
                                             time.sleep(0.5)
                                             
                                        
                          else:
                              print("Alcohol Detected")
                              GPIO.output(Buzzer, True)
                              GPIO.output(relay,True)
                              GPIO.output(red_led, True)
                              GPIO.output(green_led, False)
                              
                              time.sleep(0.5)
     
                else:
                    print("Seat belt not worn")
                    GPIO.output(Buzzer, True)
                    GPIO.output(red_led, True)
                    #GPIO.output(green_led, False)
                    time.sleep(0.5)



'''

GPIO.setmode(GPIO.BOARD)
GPIO.setup(sensor,GPIO.IN)
GPIO.setup(buzzer,GPIO.OUT)

GPIO.output(buzzer,False)
#print ("IR Sensor Ready.....")
#print (" ")

#try: 
   #while True:
     


except KeyboardInterrupt:
    GPIO.cleanup()




 
#GPIO SETUP
channel = 35
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)
 
def callback(channel):
        if GPIO.input(channel):
                print "Movement Detected!"
        else:
                print "Movement Detected!"
 
GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300)  # let us know when the pin goes HIGH or LOW
GPIO.add_event_callback(channel, callback)  # assign function to GPIO PIN, Run function on change
 
# infinite loop
while True:
        time.sleep(1)
'''