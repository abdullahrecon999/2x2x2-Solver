import cv2 
import numpy as np

url = 'http://192.168.18.11:8080/video'
cap = cv2.VideoCapture(0)

while(True):
    ret, frame = cap.read()
    frame = cv2.resize(frame,(700,500))
    #frame = cv2.rotate(frame,cv2.ROTATE_90_CLOCKWISE)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_blue = np.array([80,20,20])
    upper_blue = np.array([110,255,255])
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)

    lower_red = np.array([150,20,20])
    upper_red = np.array([190,255,255])
    mask_red = cv2.inRange(hsv, lower_red, upper_red)

    lower_yellow = np.array([20,20,20])
    upper_yellow = np.array([45,255,255])
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)

    lower_green = np.array([45,20,200])
    upper_green = np.array([65,255,255])
    mask_green = cv2.inRange(hsv, lower_green, upper_green)

    lower_orange = np.array([10,20,200])
    upper_orange = np.array([25,255,255])
    mask_orange = cv2.inRange(hsv, lower_orange, upper_orange)

    lower_white= np.array([0,0,160])
    upper_white = np.array([170,110,255])
    mask_white = cv2.inRange(hsv, lower_white, upper_white)

    mask = mask_blue + mask_red + mask_yellow + mask_green + mask_orange + mask_white

    res = cv2.bitwise_and(frame,frame, mask= mask)

    if frame is not None:
        cv2.imshow('frame',frame)
        cv2.imshow('mask',mask)
        cv2.imshow('res',res)

    q = cv2.waitKey(1)
    if q == ord("q"):
        break
cv2.destroyAllWindows()