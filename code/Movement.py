import RPi.GPIO as GPIO
import time

#If IN1=True and IN2=False right motor move forward, If IN1=False,IN2=True right motor move backward,in other cases right motor stop
IN1 = 16 #GPIO23 to IN1  right wheel direction 
IN2 = 18 #GPIO24 to IN2  right wheel direction

#If IN3=True and IN3=False left motor move forward, If IN3=False,IN4=True left motor move backward,in other cases left motor stop
IN3 = 13 #GPIO27 to IN3  left wheel direction
IN4 = 15 #GPIO22 to IN4  left wheel direction

#ENA/ENB are PWM(analog) signal pin which control the speed of right/left motor through GPIO ChangeDutyCycle(speed) function
ENA = 12 #GPIO18 to ENA PWM SPEED of right motor
ENB = 33 #GPIO13 to ENB PWM SPEED of left motor

#initialize GPIO pins, tell OS which pins will be used to control Model-Pi L298N board
GPIO.setmode(GPIO.BOARD)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(ENB, GPIO.OUT)

#Initialize ENA and ENB pins, tell OS that ENA,ENB will output analog PWM signal with 1000 frequency
rightmotor = GPIO.PWM(ENA,1000)	
leftmotor = GPIO.PWM(ENB,1000)	
rightmotor.start(0)
leftmotor.start(0)

#make both motor moving forward
def go_ahead(speed):
    GPIO.output(IN1,True)
    GPIO.output(IN2,False)
    GPIO.output(IN3,True)
    GPIO.output(IN4,False)

    #ChangeDutyCycle(speed) function can change the motor rotation speed
    rightmotor.ChangeDutyCycle(speed)
    leftmotor.ChangeDutyCycle(speed)
    
    #make both motor moving backward
def go_back(speed):
    GPIO.output(IN2,True)
    GPIO.output(IN1,False)
    GPIO.output(IN4,True)
    GPIO.output(IN3,False) 
    rightmotor.ChangeDutyCycle(speed)
    leftmotor.ChangeDutyCycle(speed)
    
#making left motor moving forward,right motor no movement    
def turn_left(speed):
    GPIO.output(IN2,False)
    GPIO.output(IN1,False)
    GPIO.output(IN3,True)
    GPIO.output(IN4,False) 
    leftmotor.ChangeDutyCycle(speed)
    
#make right motor moving forward and left motor no movement
def turn_right(speed):
    GPIO.output(IN1,True)
    GPIO.output(IN2,False)
    GPIO.output(IN4,False)
    GPIO.output(IN3,False)
    rightmotor.ChangeDutyCycle(speed)

#make both motor stop
def stop_car():
    GPIO.output(IN2,False)
    GPIO.output(IN1,False)
    GPIO.output(IN3,False)
    GPIO.output(IN4,False)

#uncomment to turn right
#turn_right(40)
#time.sleep(.6)
#stop_car()

#uncomment to turn left
#turn_left(40)
#time.sleep(.6)
#stop_car()

#uncomment to reverse
#go_back(40)
#time.sleep(.6)
#stop_car()

go_ahead(40)
time.sleep(.8)
stop_car()


GPIO.cleanup()    
