import cv2
import numpy as np
import KnnColor
import statistics as st

# initialize the cv2 object as a video frame
url = 'http://192.168.18.11:8080/video'
cap = cv2.VideoCapture(0) 

# setting the size of the video window
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 800)


# defining the middle coordinates to place the rectangles
upper_left = (300, 100)
bottom_right = (540, 340)

# the center of the box drawn in the middle
center = (int(((upper_left[0]+bottom_right[0])/2)),int((upper_left[1]+bottom_right[1])/2))
offset = 50

# defining the coordinates for the rectangles in the secondary screen
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


# defining coordinates for the arrow
turn_right_start = (165, 380)
turn_right_end = (265, 380)

turn_up_start = (530, 165)
turn_up_end = (530, 265)

turn_up_start2 = (510, 165)
turn_up_end2 = (510, 265)

# an array of strings which will display which side should the user capture now
side = ['FRONT', 'RIGHT', 'BACK', 'LEFT', 'UP', 'BOTTOM']

# Dictionary of colors for secodary screen
defaultCols = {
    'blue':  [255, 51, 19],
    'white': [249, 237, 236],
    'red':   [45, 48, 251],
    'green': [45, 251, 80 ],
    'yellow':[38, 254, 251 ],
    'orange':[17, 154, 255],
}

# declaring a 2D array to store individual side colors in each array
colors = [[0 for x in range(4)] for y in range(6)] 


# method to fill the blocks in the secondary screen
# Fixing Colors for All sides instead of printing RGB
def fillBlocks(upper_left, bottom_right, center, offset):
    fillColors()

    r1 = cv2.rectangle(colorframe, (upper_left[0]+offset,upper_left[1]+offset), (center[0]-offset,center[1]-offset), defaultCols[colors[count][0]], -1)
    r2 = cv2.rectangle(colorframe, (center[0]+offset,upper_left[1]+offset), (bottom_right[0]-offset,center[1]-offset), defaultCols[colors[count][1]], -1)
    r3 = cv2.rectangle(colorframe, (upper_left[0]+offset,center[1]+offset), (center[0]-offset,bottom_right[1]-offset), defaultCols[colors[count][2]], -1)
    r4 = cv2.rectangle(colorframe, (center[0]+offset,center[1]+offset), (bottom_right[0]-offset,bottom_right[1]-offset), defaultCols[colors[count][3]], -1)


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
        colors[count][cube] = classifier.PredictColor(CubeCols[i][0],CubeCols[i][1],CubeCols[i][2])
        cube += 1
    print(colors)

def showArrow(st_coor, end_coor):
    print('do something')
    cv2.arrowedLine(colorframe, st_coor, end_coor, (255,255,255), 5)

def remArrow(st_coor, end_coor):
    cv2.arrowedLine(colorframe, st_coor, end_coor, (0,0,0), 5)
    



def MarkSide(upper_left, bottom_right, add):
    if(add == 1):
        cv2.rectangle(colorframe, (upper_left[0],upper_left[1]), (bottom_right[0],bottom_right[1]), (255,255,255), 1)
    elif(add == 0):
        cv2.rectangle(colorframe, (upper_left[0],upper_left[1]), (bottom_right[0],bottom_right[1]), (0,0,0), 1)

def main():

    # variable to increment and decrement according to the user input and to be used for color
    # capturing and filling the blocks in the second screen and also capturing colors from the block
    global count
    count = 0

    # text to display the side for user experience
    text = ''
    
    # creating an array of 500x500 pixels to be used in frames
    # global colorFrame
    colorFrame = np.zeros(shape=[430, 550, 3], dtype=np.uint8)
    global colorframe
    colorframe = cv2.rectangle(colorFrame, (0,0), (430,550), (0,0,0), 1)

    count1=0
    sq1 = list()
    sq2 = list()
    sq3 = list()
    sq4 = list()

    while(True):
        # start reading the camera
        global frame
        _, frame = cap.read()
        #frame = cv2.flip(frame,1)

        # central rectangle to fit smaller rectangles in
        global rectMark
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

        # splitting the bgr channels from each cube and appending it into an array
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
                'ALIGN ' + text + 'FACE', 
                (50,50), 
                font, 2, 
                (255, 255, 255), 
                2,
                cv2.LINE_4)

        CubeCols = {
            'C0':[cv2.mean(cubeCols[0][0])[0], cv2.mean(cubeCols[0][1])[0], cv2.mean(cubeCols[0][2])[0]],
            'C1':[cv2.mean(cubeCols[1][0])[0], cv2.mean(cubeCols[1][1])[0], cv2.mean(cubeCols[1][2])[0]],
            'C2':[cv2.mean(cubeCols[2][0])[0], cv2.mean(cubeCols[2][1])[0], cv2.mean(cubeCols[2][2])[0]],
            'C3':[cv2.mean(cubeCols[3][0])[0], cv2.mean(cubeCols[3][1])[0], cv2.mean(cubeCols[3][2])[0]]
        }

        sq1.append(classifier.PredictColor(CubeCols['C0'][0],CubeCols['C0'][1],CubeCols['C0'][2]))
        sq2.append(classifier.PredictColor(CubeCols['C1'][0],CubeCols['C1'][1],CubeCols['C1'][2]))
        sq3.append(classifier.PredictColor(CubeCols['C2'][0],CubeCols['C2'][1],CubeCols['C2'][2]))
        sq4.append(classifier.PredictColor(CubeCols['C3'][0],CubeCols['C3'][1],CubeCols['C3'][2]))
        count1 +=1

        if count1 == 5:
            count1 = 0
            print("------------------")
            print(st.mode(sq1))
            print(st.mode(sq2))
            print(st.mode(sq3))
            print(st.mode(sq4))
            print("------------------")
            sq1.clear()
            sq2.clear()
            sq3.clear()
            sq4.clear()

        #show the video frame
        cv2.imshow('frame', frame)
        cv2.imshow("Color Output",colorFrame)

        keypress = cv2.waitKey(1)

        # increment count variable
        if keypress & 0xFF == ord('c'):
            count = (count + 1) % 6
            print(count)

        # decrement count
        if keypress & 0xFF == ord('x'):
            count = (count - 1) % 6
            print(count)
    
        # Function to highlight the current side
        if(count == 0):
            MarkSide(bottom_up, bottom_down, 0)
            MarkSide(front_up, front_down, 1)
            MarkSide(right_up, right_down, 0)
            remArrow(turn_right_end, turn_right_start)
            remArrow(turn_up_start, turn_up_end)
            remArrow(turn_up_end2, turn_up_start2)
            remArrow(turn_up_end, turn_up_start)
        elif(count == 1):
            MarkSide(front_up, front_down, 0)
            MarkSide(right_up, right_down, 1)
            MarkSide(back_up, back_down, 0)
            showArrow(turn_right_end, turn_right_start)
            remArrow(turn_up_end2, turn_up_start2)
            remArrow(turn_up_start, turn_up_end)
            remArrow(turn_up_end, turn_up_start)
        elif(count == 2):
            MarkSide(right_up, right_down, 0)
            MarkSide(back_up, back_down, 1)
            MarkSide(left_up, left_down, 0)
            showArrow(turn_right_end, turn_right_start)
            remArrow(turn_up_end2, turn_up_start2)
            remArrow(turn_up_start, turn_up_end)
            remArrow(turn_up_end, turn_up_start)
        elif(count == 3):
            MarkSide(back_up, back_down, 0)
            MarkSide(left_up, left_down, 1)
            MarkSide(top_up, top_down, 0)
            showArrow(turn_right_end, turn_right_start)
            remArrow(turn_up_end2, turn_up_start2)
            remArrow(turn_up_start, turn_up_end)
            remArrow(turn_up_end, turn_up_start)
        elif(count == 4):
            MarkSide(left_up, left_down, 0)
            MarkSide(top_up, top_down, 1)
            MarkSide(bottom_up, bottom_down, 0)
            remArrow(turn_up_end, turn_up_start)
            showArrow(turn_up_start, turn_up_end)
            remArrow(turn_up_end2, turn_up_start2)
            remArrow(turn_right_end, turn_right_start)
        else:
            MarkSide(top_up, top_down, 0)
            MarkSide(bottom_up, bottom_down, 1)
            MarkSide(front_up, front_down, 0)
            remArrow(turn_up_start, turn_up_end)
            showArrow(turn_up_end, turn_up_start)
            showArrow(turn_up_end2, turn_up_start2)
            remArrow(turn_right_end, turn_right_start)




        # capture, store and display colors 
        if keypress == 13:
            print('enter pressed')
            if(count == 0):
                print('filling front block')
                fillBlocks(front_up, front_down, cen_f, offset2)
                count = (count + 1) % 6
            elif(count == 1):
                fillBlocks(right_up, right_down, cen_r, offset2)
                count = (count + 1) % 6
            elif(count == 2):
                fillBlocks(back_up, back_down, cen_b, offset2)
                count = (count + 1) % 6
            elif(count == 3):
                fillBlocks(left_up, left_down, cen_l, offset2)
                count = (count + 1) % 6
            elif(count == 4):
                fillBlocks(top_up, top_down, cen_t, offset2)
                count = (count + 1) % 6
            else:
                fillBlocks(bottom_up, bottom_down, cen_bt, offset2)

        #press q or 1 to quit
        if keypress & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def calibrate():
    pass

if __name__ == "__main__":
    #main()
    global classifier
    classifier = KnnColor.KnnClassifier(2)
    main()
    #print(classifier.PredictColor( 62, 120, 130 ))
    for i in colors:
        print(i)


    

