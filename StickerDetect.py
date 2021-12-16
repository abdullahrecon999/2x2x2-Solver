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
center = (int(((upper_left[0]+bottom_right[0])/2)),int((upper_left[1]+bottom_right[1])/2))
offset = 20
while True:
    _, image_frame = cam_capture.read()
    
    #Rectangle marker
    r = cv2.rectangle(image_frame, upper_left, bottom_right, (0, 0, 0), 2)

    r1 = cv2.rectangle(r, (upper_left[0]+offset,upper_left[1]+offset), (center[0]-offset,center[1]-offset), (0, 0, 0), 1)
    r2 = cv2.rectangle(r, (center[0]+offset,upper_left[1]+offset), (bottom_right[0]-offset,center[1]-offset), (0, 0, 0), 1)
    r3 = cv2.rectangle(r, (upper_left[0]+offset,center[1]+offset), (center[0]-offset,bottom_right[1]-offset), (0, 0, 0), 1)
    r4 = cv2.rectangle(r, (center[0]+offset,center[1]+offset), (bottom_right[0]-offset,bottom_right[1]-offset), (0, 0, 0), 1)

    rect_img = image_frame[upper_left[1] : bottom_right[1], upper_left[0] : bottom_right[0]] # multiple of these for every r
    
    sketcher_rect = rect_img    # Multiple for every r -------------
    sketcher_rect = sketch_transform(sketcher_rect)

    sketcher_rect_rgb = cv2.bitwise_and(rect_img,rect_img)
    b = sketcher_rect_rgb[:, :, :1]
    g = sketcher_rect_rgb[:, :, 1:2]
    r = sketcher_rect_rgb[:, :, 2:]
  
    # computing the mean
    b_mean = np.mean(b)
    g_mean = np.mean(g)
    r_mean = np.mean(r)
  
    # displaying the most prominent color
    if (b_mean > g_mean and b_mean > r_mean):
        print("Blue")
    if (g_mean > r_mean and g_mean > b_mean):
        print("Green")
    else:
        print("Red")
    #sketcher_rect_rgb = cv2.bitwise_and(rect_img,rect_img)

    #Replacing the sketched image on Region of Interest
    image_frame[upper_left[1] : bottom_right[1], upper_left[0] : bottom_right[0]] = sketcher_rect_rgb
    cv2.imshow("Sketcher ROI", image_frame)
    if cv2.waitKey(1) == 13:
        break
        
cam_capture.release()
cv2.destroyAllWindows()