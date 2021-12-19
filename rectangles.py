import cv2
import numpy as np


# initialize the cv2 object as a video frame
cap = cv2.VideoCapture(0) 

# setting the size of the video window
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 800)


# defining the middle coordinates to place the rectangles
upper_left = (300, 100)
bottom_right = (540, 340)

# the center of the box drawn in the middle
center = (int(((upper_left[0]+bottom_right[0])/2)),int((upper_left[1]+bottom_right[1])/2))
offset = 25

# defining the coordinates for teh rectangles in the secondary screen
offset2 = 5

left_up = (1, 150)
left_down = (101, 250)
cen_l = (int(((left_up[0]+left_down[0])/2)),int((left_up[1]+left_down[1])/2))

front_up = (102, 150)
front_down = (202, 250)
cen_f = (int(((front_up[0]+front_down[0])/2)),int((front_up[1]+front_down[1])/2))

right_up = (203, 150)
right_down = (303, 250)
cen_r = (int(((right_up[0]+right_down[0])/2)),int((right_up[1]+right_down[1])/2))

back_up = (304, 150)
back_down = (404, 250)
cen_b = (int(((back_up[0]+back_down[0])/2)),int((back_up[1]+back_down[1])/2))

top_up = (102, 49)
top_down = (202, 149)
cen_t = (int(((top_up[0]+top_down[0])/2)),int((top_up[1]+top_down[1])/2))

bottom_up = (102, 251)
bottom_down = (202, 351)
cen_bt = (int(((bottom_up[0]+bottom_down[0])/2)),int((bottom_up[1]+bottom_down[1])/2))

# font for text on screen
font = cv2.FONT_HERSHEY_SIMPLEX


# an array of strings which will display which side should the user capture now
side = ['FRONT', 'RIGHT', 'BACK', 'LEFT', 'UP', 'BOTTOM']


# declaring a 2D array to store individual side colors in each array
colors = [[0 for x in range(4)] for y in range(6)] 


# method to differentiate colors based on a range
def getcolor(r,g,b):
    # blue
    if (r >= 118 and r <= 230 ) and (g >= 60 and g <= 174) and (b > 15 and b < 130):
        return 'b'
    # white
    elif (r >= 148 and r <= 250 ) and (g >= 140 and g < 250) and (b >= 140 and b < 250):
        return 'w'
    # yellow
    elif (r >= 21 and r <= 118 ) and (g > 130 and g < 255) and (b > 150 and b < 255):
        return 'y'
    # orange
    elif (r > 0 and r <= 75 ) and (g >= 79 and g <= 130) and (b > 125 and b < 255):
        return 'o'
    # red
    elif (r >= 10 and r <= 70 ) and (g >= 20 and g < 79) and (b >= 90 and b < 255):
        return 'r'
    # green
    elif (r >= 40 and r <= 116 ) and (g > 130 and g <= 235) and (b > 80  and b <= 170):
        return 'g'
    else:
        pass


# method to fill the blocks in the secondary screen
def fillBlocks(upper_left, bottom_right, center, offset):
    fillColors()
    r1 = cv2.rectangle(colorframe, (upper_left[0]+offset,upper_left[1]+offset), (center[0]-offset,center[1]-offset), (cv2.mean(cubeCols[0][0])[0] ,cv2.mean(cubeCols[0][1])[0] ,cv2.mean(cubeCols[0][2])[0]), -1)
    r2 = cv2.rectangle(colorframe, (center[0]+offset,upper_left[1]+offset), (bottom_right[0]-offset,center[1]-offset), (cv2.mean(cubeCols[1][0])[0] ,cv2.mean(cubeCols[1][1])[0] ,cv2.mean(cubeCols[1][2])[0]), -1)
    r3 = cv2.rectangle(colorframe, (upper_left[0]+offset,center[1]+offset), (center[0]-offset,bottom_right[1]-offset), (cv2.mean(cubeCols[2][0])[0] ,cv2.mean(cubeCols[2][1])[0] ,cv2.mean(cubeCols[2][2])[0]), -1)
    r4 = cv2.rectangle(colorframe, (center[0]+offset,center[1]+offset), (bottom_right[0]-offset,bottom_right[1]-offset), (cv2.mean(cubeCols[3][0])[0] ,cv2.mean(cubeCols[3][1])[0] ,cv2.mean(cubeCols[3][2])[0]), -1)


# method to fill the array with colors
def fillColors():
    # finding the mean of the rgb values extracted from the cubes and adding it to the dictionary
    CubeCols = {
        'C0':[cv2.mean(cubeCols[0][0])[0], cv2.mean(cubeCols[0][1])[0], cv2.mean(cubeCols[0][2])[0]],
        'C1':[cv2.mean(cubeCols[1][0])[0], cv2.mean(cubeCols[1][1])[0], cv2.mean(cubeCols[1][2])[0]],
        'C2':[cv2.mean(cubeCols[2][0])[0], cv2.mean(cubeCols[2][1])[0], cv2.mean(cubeCols[2][2])[0]],
        'C3':[cv2.mean(cubeCols[3][0])[0], cv2.mean(cubeCols[3][1])[0], cv2.mean(cubeCols[3][2])[0]]
    }
    cube = 0
    for i in CubeCols:
        colors[count][cube] = getcolor(CubeCols[i][0],CubeCols[i][1],CubeCols[i][2])
        cube += 1
    print(colors)



def main():

    # variable to increment and decrement according to the user input and to be used for color
    # capturing and filling the blocks in the second screen and also capturing colors from the block
    global count
    count = 0

    # text to display the side for user experience
    text = ''
    
    # creating an array of 500x500 pixels to be used in frames
    # global colorFrame
    colorFrame = np.zeros(shape=[400, 405, 3], dtype=np.uint8)
    global colorframe
    colorframe = cv2.rectangle(colorFrame, (0,0), (400,405), (0,0,0), 1)

    while(True):
        # start reading the camera
        _, frame = cap.read()
        frame = cv2.flip(frame,1)

        

        # central rectangle to fit smaller rectangles in
        rectMark = cv2.rectangle(frame, upper_left, bottom_right, (255,255,255), 2)

        # creating rectangles on screen for cube allignment and picking out colors
        r1 = cv2.rectangle(rectMark, (upper_left[0]+offset,upper_left[1]+offset), (center[0]-offset,center[1]-offset), (255,255,255), 1)
        r2 = cv2.rectangle(rectMark, (center[0]+offset,upper_left[1]+offset), (bottom_right[0]-offset,center[1]-offset), (255,255,255), 1)
        r3 = cv2.rectangle(rectMark, (upper_left[0]+offset,center[1]+offset), (center[0]-offset,bottom_right[1]-offset), (255,255,255), 1)
        r4 = cv2.rectangle(rectMark, (center[0]+offset,center[1]+offset), (bottom_right[0]-offset,bottom_right[1]-offset), (255,255,255), 1)

        # extracting individual pixels of allignment rectangles from the video frame
        rect_img1 = frame[upper_left[1]+offset : center[1]-offset, upper_left[0]+offset : center[0]-offset]
        rect_img2 = frame[upper_left[1]+offset : center[1]-offset, center[0]+offset : bottom_right[0]-offset]
        rect_img3 = frame[center[1]+offset : bottom_right[1]-offset, upper_left[0]+offset : center[0]-offset]
        rect_img4 = frame[center[1]+offset : bottom_right[1]-offset, center[0]+offset : bottom_right[0]-offset]

        # reassigning the individual rectangles
        Cube1 = rect_img1
        Cube2 = rect_img2
        Cube3 = rect_img3
        Cube4 = rect_img4

        # splitting the rgb channels from each cube and appending it into an array
        global cubeCols
        cubeCols = list()
        cubeCols.append(list(cv2.split(Cube1)))
        cubeCols.append(list(cv2.split(Cube2)))
        cubeCols.append(list(cv2.split(Cube3)))
        cubeCols.append(list(cv2.split(Cube4)))
        # print(cv2.mean(cubeCols[0][0])[0]) 

        

        
        # reinitializing the side text according to count
        text = side[count]


        # adding text to the cv2 video frame
        cv2.putText(frame, 
                'ALIGN ' + text + 'SIDE AND PRESS ENTER', 
                (50, 50), 
                font, 1, 
                (255, 255, 255), 
                2, 
                cv2.LINE_4)

        # for i in CubeCols:
            # print(i," : ",getcolor(CubeCols[i][0],CubeCols[i][1],CubeCols[i][2]))

        #show the video frame
        cv2.imshow('frame', frame)
        cv2.imshow("Color Output",colorFrame)
        # cv2.imshow('color output', colorFrame)

        # increment count variable
        if cv2.waitKey(1) & 0xFF == ord('c'):
            count += 1
            if(count > 5):
                count = 0
            print(count)

        # decrement count
        if cv2.waitKey(1) & 0xFF == ord('x'):
            if(count >= 0):
                count -= 1
            print(count)
    
        # capture, store and display colors 
        if cv2.waitKey(1) == 13:
            print('enter pressed')
            if(count == 0):
                print('filling front block')
                fillBlocks(front_up, front_down, cen_f, offset2)
            elif(count == 1):
                fillBlocks(right_up, right_down, cen_r, offset2)
            elif(count == 2):
                fillBlocks(back_up, back_down, cen_b, offset2)
            elif(count == 3):
                fillBlocks(left_up, left_down, cen_l, offset2)
            elif(count == 4):
                fillBlocks(top_up, top_down, cen_t, offset2)
            else:
                fillBlocks(bottom_up, bottom_down, cen_bt, offset2)

        #press q or 1 to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()



def calibrate():
    pass

main()



    

