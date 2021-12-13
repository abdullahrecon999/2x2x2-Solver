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

cam_capture = cv2.VideoCapture(0)
cv2.destroyAllWindows()
upper_left = (50, 50)
bottom_right = (300, 300)
while True:
    _, image_frame = cam_capture.read()
    
    #Rectangle marker
    r = cv2.rectangle(image_frame, upper_left, bottom_right, (100, 50, 200), 3)
    rect_img = image_frame[upper_left[1] : bottom_right[1], upper_left[0] : bottom_right[0]]
    
    sketcher_rect = rect_img
    sketcher_rect = sketch_transform(sketcher_rect)
    
    #Conversion for 3 channels to put back on original image (streaming)
    #sketcher_rect_rgb = cv2.cvtColor(sketcher_rect, cv2.COLOR_GRAY2RGB)
    sketcher_rect_rgb = cv2.bitwise_and(rect_img,rect_img, mask= sketcher_rect)
    
    #Replacing the sketched image on Region of Interest
    image_frame[upper_left[1] : bottom_right[1], upper_left[0] : bottom_right[0]] = sketcher_rect_rgb
    cv2.imshow("Sketcher ROI", image_frame)
    if cv2.waitKey(1) == 13:
        break
        
cam_capture.release()
cv2.destroyAllWindows()