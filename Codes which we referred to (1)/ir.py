import RPi.GPIO as gp  
gp.setmode(gp.BOARD)  
gp.setup(33,gp.IN)  
gp.setup(32,gp.OUT)  
gp.setup(36,gp.OUT)  
while True:
    if (gp.input(33)==False):
        print(True)
        break
    else:
        print(False)
   #print(not gp.input(33))  
