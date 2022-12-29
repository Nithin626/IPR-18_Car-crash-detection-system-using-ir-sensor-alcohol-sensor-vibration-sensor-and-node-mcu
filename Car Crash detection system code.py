#!/usr/bin/python
import time
import RPi.GPIO as GPIO
import serial
import string
import pynmea2
import serial
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

ser=serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=1)

'''
define pin for lcd
'''
# Timing constants

# Define GPIO to LCD mapping
'''LCD_RS = 7
LCD_E  = 11
LCD_D4 = 12
LCD_D5 = 13
LCD_D6 = 15
LCD_D7 = 16'''
alcohol_Sensor = 18
Buzzer= 5
switch =22
red_led=31
green_led=32
seat_belt_Sensor = 33
vibration_sensor = 35
relay = 36

GPIO.setup(alcohol_Sensor, GPIO.IN)
GPIO.setup(Buzzer, GPIO.OUT)
GPIO.setup(switch, GPIO.IN)
GPIO.setup(red_led, GPIO.OUT)
GPIO.setup(green_led, GPIO.OUT)
GPIO.setup(seat_belt_Sensor, GPIO.IN) 
GPIO.setup(vibration_sensor, GPIO.IN) 
GPIO.setup(relay , GPIO.OUT)
print("Welcome\nAlcohol Detection System")

time.sleep(1)
car_start =0
GPIO.output(Buzzer, False)
GPIO.output(green_led, False)
GPIO.output(red_led, False)
GPIO.output(relay, False)
while 1:       
    # Print out results
    car_start = 0
    alcohol_data =  GPIO.input(alcohol_Sensor)
    seat_belt_data =  GPIO.input(seat_belt_Sensor)
    if(seat_belt_data == False):
        GPIO.output(Buzzer,True)
        print ("Seat belt worn")
        
        time.sleep(0.5)
        if(alcohol_data == True):
            print(" Alcohol Not Detected !")
            
            GPIO.output(Buzzer, False)
            GPIO.output(green_led, True)
            GPIO.output(red_led, False)
            time.sleep(0.5)
            while(1):
                
                if(car_start == 0):
                    GPIO.output(relay, False)
                    print("press the switch")
                    time.sleep(0.5)
                    switch_data =GPIO.input(switch)
                    
                vibration_data =  GPIO.input(vibration_sensor)
                
                if(vibration_data == GPIO.HIGH):
                    print("Accident Detected\nLocation sent to BLYNK server")
                    
                    GPIO.output(relay, False)
                    time.sleep(2)
                    while(1):
                        dataout =pynmea2.NMEAStreamReader() 
                        newdata=ser.readline()
                        if '$GPRMC' in str(newdata):
                            print(newdata.decode('utf-8'))
                            newmsg=pynmea2.parse(newdata.decode('utf-8'))  
                            lat=newmsg.latitude 
                            lng=newmsg.longitude 
                            gps = "Latitude=" + str(lat) + "and Longitude=" +str(lng)
                            print(gps)
                            time.sleep(2)
                            '''ser.write("AT+CMGF=1\r\n".encode());    #Sets the GSM Module in Text Mode
                            time.sleep(2);  # time.sleep of 1 milli seconds or 1 second
                            ser.write("AT+CMGS=\"+919763365197\"\r\n".encode()); # Replace x with mobile number
                            time.sleep(2);
                            ser.write("Accident Detected please find location below\r\n".encode());# The SMS text you want to send
                            ser.write("lattitude:".encode());# The SMS text you want to send
                            ser.write(str(lat).encode());# The SMS text you want to send
                            ser.write("longitude:".encode());# The SMS text you want to send
                            ser.write(str(lng).encode());
                            time.sleep(2);
                            ser.write("\x1A".encode());# ASCII code of CTRL+Z
                            time.sleep(2);
                            print("send")'''
                elif(switch_data == True):
                    print("vehicle start ")
                    
                    GPIO.output(relay, True)
                    car_start = 1
                    time.sleep(0.5)
        else:
            print("Alcohol Detected")
            GPIO.output(Buzzer, True)
            GPIO.output(red_led, True)
            GPIO.output(green_led, False)
            time.sleep(0.5)
    else:
        print("Seat belt not worn") 
        GPIO.output(Buzzer, True)
        GPIO.output(red_led, True)
        GPIO.output(green_led, False)
        time.sleep(0.5)      
