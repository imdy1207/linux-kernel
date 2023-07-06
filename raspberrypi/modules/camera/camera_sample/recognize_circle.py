import cv2 as cv
import RPi.GPIO as rg
from datetime import datetime
import time

videoCapture = cv.VideoCapture(0)

led_pin = 27
rg.setmode(rg.BCM)
rg.setup(led_pin, rg.OUT)

while True:
    keycode = cv.waitKey() #키 입력을 받는다
    if keycode == ord('q') or keycode == 27 : #받은 키의 값이 q 혹은 esc 일 경우 종료 
        break

    ret, frame = videoCapture.read()
    if not ret: break

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray, (15,15), 0)

    circles = cv.HoughCircles(blur, cv.HOUGH_GRADIENT, 2, 100, param1=100, param2=100, minRadius=35, maxRadius=500)

    if circles is not None: #원이 인식된 경우
        print(circles)
        rg.output(led_pin, rg.HIGH) #LED에 불을 켠다

    else : #인식이 되지 않은 경우
        rg.output(led_pin, rg.LOW) #LED에 불을 끈다

videoCapture.release()
