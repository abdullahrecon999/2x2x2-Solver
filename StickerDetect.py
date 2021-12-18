import cv2
import numpy as np
import KnnColor

def getcolor(r,g,b):
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

def main():
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
        #image_frame = cv2.resize(image_frame,(700,500))
        colorFrame = np.zeros(shape=[500, 500, 3], dtype=np.uint8)

        rectMark = cv2.rectangle(image_frame, upper_left, bottom_right, (0, 0, 0), 2)

        r1 = cv2.rectangle(rectMark, (upper_left[0]+offset,upper_left[1]+offset), (center[0]-offset,center[1]-offset), (0, 0, 0), 1)
        r2 = cv2.rectangle(rectMark, (center[0]+offset,upper_left[1]+offset), (bottom_right[0]-offset,center[1]-offset), (0, 0, 0), 1)
        r3 = cv2.rectangle(rectMark, (upper_left[0]+offset,center[1]+offset), (center[0]-offset,bottom_right[1]-offset), (0, 0, 0), 1)
        r4 = cv2.rectangle(rectMark, (center[0]+offset,center[1]+offset), (bottom_right[0]-offset,bottom_right[1]-offset), (0, 0, 0), 1)

        rect_img1 = image_frame[upper_left[1]+offset : center[1]-offset, upper_left[0]+offset : center[0]-offset]
        rect_img2 = image_frame[upper_left[1]+offset : center[1]-offset, center[0]+offset : bottom_right[0]-offset]
        rect_img3 = image_frame[center[1]+offset : bottom_right[1]-offset, upper_left[0]+offset : center[0]-offset]
        rect_img4 = image_frame[center[1]+offset : bottom_right[1]-offset, center[0]+offset : bottom_right[0]-offset]

        Cube1 = rect_img1
        Cube2 = rect_img2
        Cube3 = rect_img3
        Cube4 = rect_img4

        #sketcher_rect = sketch_transform(sketcher_rect)
        #Cube1 = cv2.bitwise_and(rect_img1,rect_img1)

        # r,g,b = cv2.split(Cube1)
        # b_mean = cv2.mean(b)[0]
        # g_mean = cv2.mean(g)[0]
        # r_mean = cv2.mean(r)[0]

        cubeCols = list()
        cubeCols.append(list(cv2.split(Cube1)))
        cubeCols.append(list(cv2.split(Cube2)))
        cubeCols.append(list(cv2.split(Cube3)))
        cubeCols.append(list(cv2.split(Cube4)))
        #print(cv2.mean(cubeCols[0][0])[0])      #[0] cube 0 , [0] red, [0] for mean

        CubeCols = {
            'C0':[cv2.mean(cubeCols[0][0])[0] ,cv2.mean(cubeCols[0][1])[0] ,cv2.mean(cubeCols[0][2])[0]],
            'C1':[cv2.mean(cubeCols[1][0])[0],cv2.mean(cubeCols[1][1])[0] ,cv2.mean(cubeCols[1][2])[0]],
            'C2':[cv2.mean(cubeCols[2][0])[0], cv2.mean(cubeCols[2][1])[0], cv2.mean(cubeCols[2][2])[0]],
            'C3':[cv2.mean(cubeCols[3][0])[0], cv2.mean(cubeCols[3][1])[0], cv2.mean(cubeCols[3][2])[0]]
        }

        colorframe = cv2.rectangle(colorFrame, (1,1), (500,500), (0, 0, 0), -1)
        colordetect1 = cv2.rectangle(colorframe, (10,10), (100,100), (cv2.mean(cubeCols[0][0])[0] ,cv2.mean(cubeCols[0][1])[0] ,cv2.mean(cubeCols[0][2])[0]), -1)
        colordetect2 = cv2.rectangle(colorframe, (120,10), (210,100), (cv2.mean(cubeCols[1][0])[0],cv2.mean(cubeCols[1][1])[0] ,cv2.mean(cubeCols[1][2])[0]), -1)
        colordetect3 = cv2.rectangle(colorframe, (10,120), (100,210), (cv2.mean(cubeCols[2][0])[0], cv2.mean(cubeCols[2][1])[0], cv2.mean(cubeCols[2][2])[0]), -1)
        colordetect4 = cv2.rectangle(colorframe, (120,120), (210,210), (cv2.mean(cubeCols[3][0])[0], cv2.mean(cubeCols[3][1])[0], cv2.mean(cubeCols[3][2])[0]), -1)

        for i in CubeCols:
            print(i," : ",classifier.PredictColor(CubeCols[i][0],CubeCols[i][1],CubeCols[i][2]))

        image_frame[upper_left[1]+offset : center[1]-offset, upper_left[1]+offset : center[0]-offset] = Cube1
        image_frame[upper_left[1]+offset : center[1]-offset, center[0]+offset : bottom_right[0]-offset] = Cube2
        image_frame[center[1]+offset : bottom_right[1]-offset, upper_left[0]+offset : center[0]-offset] = Cube3
        image_frame[center[1]+offset : bottom_right[1]-offset, center[0]+offset : bottom_right[0]-offset] = Cube4

        cv2.imshow("Color detect", image_frame)
        cv2.imshow("Color Output",colorFrame)
        if cv2.waitKey(1) == 13:
            break
            
    cam_capture.release()
    cv2.destroyAllWindows()

def calibrate():
    pass

if __name__ == "__main__":
    #main()
    classifier = KnnColor.KnnClassifier(7)
    #classifier.CreateKNN()
    main()
    print(classifier.PredictColor( 62, 120, 130 ))