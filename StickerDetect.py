import cv2
import numpy as np
from matplotlib import pyplot as plt

def sketch_transform(frame):
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
    return mask

def getcolor(r,g,b): # compare rgb values and return color
    if (r >= 118 and r <= 230 ) and (g >= 60 and g <= 174) and (b > 15 and b < 130):
        return 'b'
    elif (r >= 148 and r <= 250 ) and (g >= 140 and g < 250) and (b >= 140 and b < 250):
        return 'w'
    elif (r >= 21 and r <= 118 ) and (g > 130 and g < 255) and (b > 150 and b < 255):
        return 'y'
    elif (r > 0 and r <= 75 ) and (g >= 79 and g <= 130) and (b > 125 and b < 255):
        return 'o'
    elif (r >= 10 and r <= 70 ) and (g >= 20 and g < 79) and (b >= 90 and b < 255):
        return 'r'
    elif (r >= 40 and r <= 116 ) and (g > 130 and g <= 235) and (b > 80  and b <= 170):
        return 'g'
    else:
        pass

url = 'http://192.168.18.11:8080/video'
cam_capture = cv2.VideoCapture(0)
cv2.destroyAllWindows()
upper_left = (50, 50)
bottom_right = (300, 300)
center = (int(((upper_left[0]+bottom_right[0])/2)),int((upper_left[1]+bottom_right[1])/2))
offset = 20

while True:
    _, image_frame = cam_capture.read()
    image_frame = cv2.flip(image_frame,1)
    colorFrame = np.zeros(shape=[500, 500, 3], dtype=np.uint8)

    #Rectangle marker
    rectMark = cv2.rectangle(image_frame, upper_left, bottom_right, (0, 0, 0), 2)

    r1 = cv2.rectangle(rectMark, (upper_left[0]+offset,upper_left[1]+offset), (center[0]-offset,center[1]-offset), (0, 0, 0), 1)
    r2 = cv2.rectangle(rectMark, (center[0]+offset,upper_left[1]+offset), (bottom_right[0]-offset,center[1]-offset), (0, 0, 0), 1)
    r3 = cv2.rectangle(rectMark, (upper_left[0]+offset,center[1]+offset), (center[0]-offset,bottom_right[1]-offset), (0, 0, 0), 1)
    r4 = cv2.rectangle(rectMark, (center[0]+offset,center[1]+offset), (bottom_right[0]-offset,bottom_right[1]-offset), (0, 0, 0), 1)

    rect_img1 = image_frame[upper_left[1]+offset : center[1]-offset, upper_left[0]+offset : center[0]-offset]
    rect_img2 = image_frame[upper_left[1]+offset : center[1]-offset, center[0]+offset : bottom_right[0]-offset]
    #rect_img3 = image_frame[upper_left[1] : bottom_right[1], upper_left[0] : bottom_right[0]]
    #rect_img4 = image_frame[upper_left[1] : bottom_right[1], upper_left[0] : bottom_right[0]]

    Cube1 = rect_img2
    #sketcher_rect = sketch_transform(sketcher_rect)
    #Cube1 = cv2.bitwise_and(rect_img1,rect_img1)

    r,g,b = cv2.split(Cube1)

    b_mean = cv2.mean(b)[0]
    g_mean = cv2.mean(g)[0]
    r_mean = cv2.mean(r)[0]

    colorframe = cv2.rectangle(colorFrame, (1,1), (500,500), (0, 0, 0), -1)

    colordetect1 = cv2.rectangle(colorframe, (10,10), (100,100), (r_mean, g_mean, b_mean), -1)
    colordetect2 = cv2.rectangle(colorframe, (120,10), (210,100), (r_mean, g_mean, b_mean), -1)
    colordetect3 = cv2.rectangle(colorframe, (10,120), (100,210), (r_mean, g_mean, b_mean), -1)
    colordetect4 = cv2.rectangle(colorframe, (120,120), (210,210), (r_mean, g_mean, 0), -1)

    print(getcolor(r_mean,g_mean,b_mean))
    
    #image_frame[upper_left[1] : bottom_right[1], upper_left[0] : bottom_right[0]] = Cube1
    #image_frame[upper_left[1]+offset : center[1]-offset, upper_left[1]+offset : center[0]-offset] = Cube1
    image_frame[upper_left[1]+offset : center[1]-offset, center[0]+offset : bottom_right[0]-offset] = Cube1

    cv2.imshow("Color detect", image_frame)
    cv2.imshow("Color Output",colorFrame)
    if cv2.waitKey(1) == 13:
        break
        
cam_capture.release()
cv2.destroyAllWindows()