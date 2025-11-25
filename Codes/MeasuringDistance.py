import cv2
import numpy as np
from scipy.stats import itemfreq
import time

import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
IN1 = 16 #GPIO23 to IN1  right wheel direction
IN2 = 18 #GPIO24 to IN2  right wheel direction

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
  
#make both motor stop
def stop_car():
    GPIO.output(IN2,False)
    GPIO.output(IN1,False)
    GPIO.output(IN3,False)
    GPIO.output(IN4,False)

def get_dominant_color(image, n_colors):
    pixels = np.float32(image).reshape((-1, 3))
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
    flags = cv2.KMEANS_RANDOM_CENTERS
    flags, labels, centroids = cv2.kmeans(pixels, n_colors, None, criteria, 10, flags)
    palette = np.uint8(centroids)
    return palette[np.argmax(itemfreq(labels)[:, -1])]

clicked = False
def onMouse(event, x, y, flags, param):
    global clicked
    if event == cv2.EVENT_LBUTTONUP:
        clicked = True

cameraCapture = cv2.VideoCapture(0)
cameraCapture.set(3,320)
cameraCapture.set(4,240)

cv2.namedWindow('camera')
cv2.setMouseCallback('camera', onMouse)

# Read and process frames in loop
success, frame = cameraCapture.read()

font = cv2.FONT_HERSHEY_SIMPLEX
similarity = 0.6
template_Dis = cv2.imread("/home/pi/Desktop/Distance.png", cv2.IMREAD_GRAYSCALE)
w_Dis, h_Dis = template_Dis.shape[::-1]

trigger = 0
start_trigger = 0
end_trigger = 0


while success and not clicked:
    distance = 0
    speed = 0.21

    cv2.waitKey(1)
    success, frame = cameraCapture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    img = cv2.medianBlur(gray, 37)
    circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT,
                              1, 390, param1=120, param2=40)


    res_Dis = cv2.matchTemplate(gray, template_Dis, cv2.TM_CCOEFF_NORMED)
    loc_Dis = np.where(res_Dis >= similarity)

    for pt in zip(*loc_Dis[::-1]):
        cv2.rectangle(frame, pt, (pt[0] + w_Dis, pt[1] + h_Dis), (0, 255, 0), 3)
        cv2.putText(frame, 'MeasureDistance', (pt[0] + w_Dis, pt[1] + h_Dis), font, 1, (0, 255, 0), 1)
        trigger = 1
        go_ahead(30)

        if start_trigger == 0:
            start_trigger = 1
            start_time = time.time()
            print("start time", start_time)


    if not circles is None:
        circles = np.uint16(np.around(circles))
        max_r, max_i = 0, 0
        for i in range(len(circles[:, :, 2][0])):
            if circles[:, :, 2][0][i] > 50 and circles[:, :, 2][0][i] > max_r:
                max_i = i
                max_r = circles[:, :, 2][0][i]
        x, y, r = circles[:, :, :][0][max_i]
        if y > r and x > r:
            square = frame[y-r:y+r, x-r:x+r]
            dominant_color = get_dominant_color(square, 2)

            if dominant_color[2] > 200:
                stop_car()
                if trigger == 1:
                    if end_trigger == 0:
                        end_trigger = 1
                        end_time = time.time()
                        distance = speed * (end_time - start_time)
                        print("end time", end_time)
                        print("distance", distance, "m")
                        exit()
                else:
                    print("STOP")
                    cv2.putText(frame, 'STOP', (x + r, y + r), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 4)
            
        for i in circles[0, :]:
            cv2.circle(frame, (i[0], i[1]), i[2], (0, 255, 0), 2)
            cv2.circle(frame, (i[0], i[1]), 2, (0, 0, 255), 3)
    
      
    cv2.imshow('camera', frame)




GPIO.cleanup()
GPIO.setwarnings(False)
cv2.destroyAllWindows()
cameraCapture.release()
