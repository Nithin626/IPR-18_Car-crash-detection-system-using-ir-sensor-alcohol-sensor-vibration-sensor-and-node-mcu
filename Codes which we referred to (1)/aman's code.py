#!/usr/bin/python
import time
import RPi.GPIO as GPIO
import serial
import string
import pynmea2
#import serial
from signal import signal,SIGTERM,SIGHUP
from rpi_lcd import LCD
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

ser=serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=1)

'''
define pin for lcd
'''
# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005
delay = 1

# Define GPIO to LCD mapping
LCD_RS = 7
LCD_E  = 11
LCD_D4 = 12
LCD_D5 = 13
LCD_D6 = 15
LCD_D7 = 16
SDA=3
SCL=5
alcohol_Sensor = 18
Buzzer= 29
switch =22
red_led=31
green_led=32
seat_belt_Sensor = 33
vibration_sensor = 35
relay = 36

GPIO.setup(LCD_E, GPIO.OUT)  # E
GPIO.setup(LCD_RS, GPIO.OUT) # RS
GPIO.setup(LCD_D4, GPIO.OUT) # DB4
GPIO.setup(LCD_D5, GPIO.OUT) # DB5
GPIO.setup(LCD_D6, GPIO.OUT) # DB6
GPIO.setup(LCD_D7, GPIO.OUT) 
GPIO.setup(SDA,GPIO.OUT)
GPIO.setup(SCL,GPIO.OUT)
GPIO.setup(alcohol_Sensor,GPIO.IN)
# GPIO.setup(Buzzer,GPIO.OUT)
GPIO.setup(switch, GPIO.IN)
GPIO.setup(red_led, GPIO.OUT)
GPIO.setup(green_led, GPIO.OUT)
GPIO.setup(seat_belt_Sensor, GPIO.IN) 
GPIO.setup(vibration_sensor, GPIO.IN) 
GPIO.setup(relay , GPIO.OUT)

# Define some device constants
LCD_WIDTH = 16    # Maximum characters per line
LCD_CHR = True
LCD_CMD = False
LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line


'''
Function Name :lcd_init()
Function Description : this function is used to initialized lcd by sending the different commands
'''
def lcd_init():
  # Initialise display
  lcd_byte(0x33,LCD_CMD) # 110011 Initialise
  lcd_byte(0x32,LCD_CMD) # 110010 Initialise
  lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
  lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
  lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
  lcd_byte(0x01,LCD_CMD) # 000001 Clear display
  time.sleep(E_DELAY)
'''
Function Name :lcd_byte(bits ,mode)
Fuction Name :the main purpose of this function to convert the byte data into bit and send to lcd port
'''
def lcd_byte(bits, mode):
  # Send byte to data pins
  # bits = data
  # mode = True  for character
  #        False for command
 
  GPIO.output(LCD_RS, mode) # RS
 
  # High bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x10==0x10:
    GPIO.output(LCD_D4, True)
  if bits&0x20==0x20:
    GPIO.output(LCD_D5, True)
  if bits&0x40==0x40:
    GPIO.output(LCD_D6, True)
  if bits&0x80==0x80:
    GPIO.output(LCD_D7, True)
 
  # Toggle 'Enable' pin
  lcd_toggle_enable()
 
  # Low bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x01==0x01:
    GPIO.output(LCD_D4, True)
  if bits&0x02==0x02:
    GPIO.output(LCD_D5, True)
  if bits&0x04==0x04:
    GPIO.output(LCD_D6, True)
  if bits&0x08==0x08:
    GPIO.output(LCD_D7, True)
 
  # Toggle 'Enable' pin
  lcd_toggle_enable()
'''
Function Name : lcd_toggle_enable()
Function Description:basically this is used to toggle Enable pin
'''
def lcd_toggle_enable():
  # Toggle enable
  time.sleep(E_DELAY)
  GPIO.output(LCD_E, True)
  time.sleep(E_PULSE)
  GPIO.output(LCD_E, False)
  time.sleep(E_DELAY)
'''
Function Name :lcd_string(message,line)
Function  Description :print the data on lcd 
'''
def lcd_string(message,line):
  # Send string to display
 
  message = message.ljust(LCD_WIDTH," ")
 
  lcd_byte(line, LCD_CMD)
 
  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)


lcd_init()
lcd_string("welcome ",LCD_LINE_1)

time.sleep(1)
lcd_byte(0x01,LCD_CMD) # 000001 Clear display
lcd_string("Accident",LCD_LINE_1)
lcd_string("Detection System",LCD_LINE_2)
signal(SIGTERM, safe_exit)
signal(SIGHUP, safe_exit)
lcd.text("Hello", 1)
lcd.text("IPR 18!", 2)
pause()
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
        lcd_byte(0x01,LCD_CMD) # 000001 Clear display
        lcd_string("Seat Belt  ",LCD_LINE_1)
        lcd_string(" Detected  ",LCD_LINE_2)
		lcd.text("Seat Belt",1)
		lcd.text("Detected",2)
        time.sleep(0.5)
        if(alcohol_data == True):
            lcd_string("Alcohol not  ",LCD_LINE_1)
            lcd_string(" Detected  ",LCD_LINE_2)
			  lcd.text("Alcohol not",1)
		     lcd.text("Detected",2)
            GPIO.output(Buzzer, False)
            GPIO.output(green_led, True)
            GPIO.output(red_led, False)
            time.sleep(0.5)
            while(1):
                lcd_byte(0x01,LCD_CMD) # 000001 Clear display
                if(car_start == 0):
                    lcd_string("press the switch",LCD_LINE_1)
						lcd.text("press the switch",1)
                    time.sleep(0.5)
                    switch_data =     GPIO.input(switch)
                    
                vibration_data =  GPIO.input(vibration_sensor)
                
                if(vibration_data == GPIO.HIGH):
                    lcd_string("Accident ",LCD_LINE_1)
                    lcd_string(" Detected  ",LCD_LINE_2)
                    GPIO.output(relay, False)
                    time.sleep(2)
                    while(1):
                        dataout =pynmea2.NMEAStreamReader() 
                        newdata=ser.readline()
                        if '$GPRMC' in str(newdata):
                            #print(newdata.decode('utf-8'))
                            newmsg=pynmea2.parse(newdata.decode('utf-8'))  
                            lat=newmsg.latitude 
                            lng=newmsg.longitude 
                            #gps = "Latitude=" + str(lat) + "and Longitude=" +str(lng)
                            #print(gps)
                            time.sleep(2)
                            ser.write("AT+CMGF=1\r\n".encode());    #Sets the GSM Module in Text Mode
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
                            print("send")
                elif(switch_data == True):
                    lcd_byte(0x01,LCD_CMD) # 000001 Clear display
                    lcd_string("vehicle start ",LCD_LINE_1)
                    GPIO.output(relay, True)
                    car_start = 1
                    time.sleep(0.5)
        else:
            lcd_string("Alcohol Detected",LCD_LINE_1)
            GPIO.output(Buzzer, True)
            GPIO.output(red_led, True)
            GPIO.output(green_led, False)
            time.sleep(0.5)
    else:
        lcd_byte(0x01,LCD_CMD) # 000001 Clear display
        lcd_string("Please Wear",LCD_LINE_1)
        lcd_string(" Seat Belt  ",LCD_LINE_2)
        GPIO.output(Buzzer, True)
        GPIO.output(red_led, True)
        GPIO.output(green_led, False)
        time.sleep(0.5)      