import cv2
import numpy as np
from scipy.stats import itemfreq

import RPi.GPIO as GPIO
import time

IN1 = 16
IN2 = 18

IN3 = 13
IN4 = 15

ENA = 12
ENB = 33

GPIO.setmode(GPIO.BOARD)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(ENB, GPIO.OUT)

rightmotor = GPIO.PWM(ENA,1000)	
leftmotor = GPIO.PWM(ENB,1000)	
rightmotor.start(0)
leftmotor.start(0)

def go_ahead(speed):
    GPIO.output(IN1,True)
    GPIO.output(IN2,False)
    GPIO.output(IN3,True)
    GPIO.output(IN4,False)

    rightmotor.ChangeDutyCycle(speed)
    leftmotor.ChangeDutyCycle(speed)

def go_back(speed):
    GPIO.output(IN2,True)
    GPIO.output(IN1,False)
    GPIO.output(IN4,True)
    GPIO.output(IN3,False) 
    rightmotor.ChangeDutyCycle(speed)
    leftmotor.ChangeDutyCycle(speed)

def turn_left(speed):
    GPIO.output(IN2,False)
    GPIO.output(IN1,False)
    GPIO.output(IN3,True)
    GPIO.output(IN4,False) 
    leftmotor.ChangeDutyCycle(speed)

def turn_right(speed):
    GPIO.output(IN1,True)
    GPIO.output(IN2,False)
    GPIO.output(IN4,False)
    GPIO.output(IN3,False)
    rightmotor.ChangeDutyCycle(speed)

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
cv2.namedWindow('camera')
cv2.setMouseCallback('camera', onMouse)

# Read and process frames in loop
success, frame = cameraCapture.read()

while success and not clicked:
    cv2.waitKey(1)
    success, frame = cameraCapture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    img = cv2.medianBlur(gray, 37)
    circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT,
                              1, 300, param1=120, param2=40)

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
            if dominant_color[2] > 110:
                print("STOP")
                cv2.putText(frame, 'STOP', (x + r, y + r), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 4)

            elif dominant_color[0] > 70:
                zone_0 = square[square.shape[0]*3//8:square.shape[0]
                                * 5//8, square.shape[1]*1//8:square.shape[1]*3//8]
                #cv2.imshow('Zone0', zone_0)
                zone_0_color = get_dominant_color(zone_0, 1)

                zone_1 = square[square.shape[0]*1//8:square.shape[0]
                                * 3//8, square.shape[1]*3//8:square.shape[1]*5//8]
                #cv2.imshow('Zone1', zone_1)
                zone_1_color = get_dominant_color(zone_1, 1)

                zone_2 = square[square.shape[0]*3//8:square.shape[0]
                                * 5//8, square.shape[1]*5//8:square.shape[1]*7//8]
                #cv2.imshow('Zone2', zone_2)
                zone_2_color = get_dominant_color(zone_2, 1)

                zone_3 = square[square.shape[0] * 5 // 8:square.shape[0]
                                * 7 // 8, square.shape[1] * 3 // 8:square.shape[1] * 5 // 8]
                #cv2.imshow('Zone3', zone_3)
                zone_3_color = get_dominant_color(zone_3, 1)


                if zone_1_color[2] < 50:
                    if sum(zone_0_color) > sum(zone_2_color):
                        print("LEFT")

                        turn_left(50)
                        time.sleep(.6)
                        stop_car()

                        cv2.putText(frame,'LEFT',(x+r,y+r),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),4)
                    else:
                        print("RIGHT")

                        turn_right(50)
                        time.sleep(.6)
                        stop_car()

                        cv2.putText(frame,'RIGHT',(x+r,y+r),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),4)
                else:
                    if sum(zone_1_color) > sum(zone_3_color):
                        print("FORWARD")
                        
                        go_ahead(40)
                        time.sleep(.5)
                        stop_car()
                        
                        cv2.putText(frame,'FORWARD',(x+r,y+r),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),4)
                    else:
                        print("REVERSE")
                        
                        go_back(40)
                        time.sleep(.5)
                        stop_car()
                        
                        cv2.putText(frame,'REVERSE',(x+r,y+r),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),4)
            else:
                print("N/A")

        for i in circles[0, :]:
            cv2.circle(frame, (i[0], i[1]), i[2], (0, 255, 0), 2)
            cv2.circle(frame, (i[0], i[1]), 2, (0, 0, 255), 3)
    cv2.imshow('camera', frame)



cv2.destroyAllWindows()
cameraCapture.release()
