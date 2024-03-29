import cv2
import numpy as np
import KnnColor
import Solver
import queue
import threading
import time
import solution
from threading import Thread
import PySimpleGUI as sg

from solution import SolutionDisplay

sg.theme('LightBrown1')
check = threading.Condition()

layout = [
    [sg.Image(filename='', key='Main'),sg.Image(filename='', key='Second')],
    [sg.Frame('Video Feed',[[sg.Text("ON"),sg.Slider(range=(0, 1), orientation='h', size=(10, 30), default_value=0,disable_number_display=True,trough_color='#566573',key='switch'),sg.Text("OFF")]]),sg.Button('Run Solution', size=(11, 3),font="ariel 13 bold"),sg.Button('Exit', size=(10, 3),font="ariel 13 bold"),sg.Button('Reset', size=(10, 3),font="ariel 13 bold")]
]

window = sg.Window('OpenCV real-time image processing',layout,location=(400, 100),finalize=True,return_keyboard_events=True, use_default_focus=False)

upper_left = (300, 100)
bottom_right = (540, 340)
center = (int(((upper_left[0]+bottom_right[0])/2)),int((upper_left[1]+bottom_right[1])/2))
offset = 35
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

# defining coordinates for the arrow
turn_right_start = (165, 380)
turn_right_end = (265, 380)

turn_up_start = (450, 165)
turn_up_end = (450, 265)

turn_up_start2 = (430, 165)
turn_up_end2 = (430, 265)

font = cv2.FONT_HERSHEY_SIMPLEX
side = ['FRONT', 'RIGHT', 'BACK', 'LEFT', 'UP', 'BOTTOM']

defaultCols = {
     0:      [255,255,255],
    'blue':  [255, 51, 19 ],
    'white': [249, 237, 236],
    'red':   [45, 48, 251],
    'green': [45, 251, 80],
    'yellow':[38, 254, 251],
    'orange':[17, 154, 255],
}

colors = [[0 for x in range(4)] for y in range(6)] 

def clearColorFrame(upper_left, bottom_right, center, offset):
    r1 = cv2.rectangle(colorframe, (upper_left[0]+offset,upper_left[1]+offset), (center[0]-offset,center[1]-offset), (0,0,0), -1)
    r2 = cv2.rectangle(colorframe, (center[0]+offset,upper_left[1]+offset), (bottom_right[0]-offset,center[1]-offset), (0,0,0), -1)
    r3 = cv2.rectangle(colorframe, (upper_left[0]+offset,center[1]+offset), (center[0]-offset,bottom_right[1]-offset), (0,0,0), -1)
    r4 = cv2.rectangle(colorframe, (center[0]+offset,center[1]+offset), (bottom_right[0]-offset,bottom_right[1]-offset), (0,0,0), -1)

def fillBlocks(upper_left, bottom_right, center, offset):
    fillColors()

    r1 = cv2.rectangle(colorframe, (upper_left[0]+offset,upper_left[1]+offset), (center[0]-offset,center[1]-offset), defaultCols[colors[count][0]], -1)
    r2 = cv2.rectangle(colorframe, (center[0]+offset,upper_left[1]+offset), (bottom_right[0]-offset,center[1]-offset), defaultCols[colors[count][1]], -1)
    r3 = cv2.rectangle(colorframe, (upper_left[0]+offset,center[1]+offset), (center[0]-offset,bottom_right[1]-offset), defaultCols[colors[count][2]], -1)
    r4 = cv2.rectangle(colorframe, (center[0]+offset,center[1]+offset), (bottom_right[0]-offset,bottom_right[1]-offset), defaultCols[colors[count][3]], -1)

def fillColors():
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

def MarkSide(upper_left, bottom_right, add):
    if(add == 1):
        cv2.rectangle(colorframe, (upper_left[0],upper_left[1]), (bottom_right[0],bottom_right[1]), (255,255,255), 1)
    elif(add == 0):
        cv2.rectangle(colorframe, (upper_left[0],upper_left[1]), (bottom_right[0],bottom_right[1]), (0,0,0), 1)

def showArrow(st_coor, end_coor):
    cv2.arrowedLine(colorframe, st_coor, end_coor, (255,255,255), 5)

def remArrow(st_coor, end_coor):
    cv2.arrowedLine(colorframe, st_coor, end_coor, (0,0,0), 5)

def main():
    Recording = True

    url = 'http://192.168.18.11:8080/video'
    cap = cv2.VideoCapture(0) 

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 700)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 700)

    global count
    count = 0
    text = ''
    
    colorFrame = np.zeros(shape=[400, 500, 3], dtype=np.uint8)
    global colorframe
    colorframe = cv2.rectangle(colorFrame, (0,0), (400,500), (0,0,0), 1)

    while(True):
        event, values = window.read(timeout=0, timeout_key='timeout')

        if(values['switch'] == 1.0 and Recording == True):
            Recording = False
            cap.release()
            frame = np.zeros(shape=[400, 405, 3], dtype=np.uint8)
            imgbytes = cv2.imencode('.png', frame)[1].tobytes()
            window['Main'].update(data=imgbytes)

        elif(values['switch'] == 0.0 and Recording == False):
            Recording = True
            cap = cv2.VideoCapture(0)
        
        if Recording:
            try:
                _, frame = cap.read()

                scale_percent = 100
                width = int(frame.shape[1] * scale_percent / 100)
                height = int(frame.shape[0] * scale_percent / 100)
                dim = (width, height)
                
                frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA )
                frame = cv2.flip(frame,1)

                rectMark = cv2.rectangle(frame, upper_left, bottom_right, (255,255,255), 2)

                r1 = cv2.rectangle(rectMark, (upper_left[0]+offset,upper_left[1]+offset), (center[0]-offset,center[1]-offset), (255,255,255), 1)
                r2 = cv2.rectangle(rectMark, (center[0]+offset,upper_left[1]+offset), (bottom_right[0]-offset,center[1]-offset), (255,255,255), 1)
                r3 = cv2.rectangle(rectMark, (upper_left[0]+offset,center[1]+offset), (center[0]-offset,bottom_right[1]-offset), (255,255,255), 1)
                r4 = cv2.rectangle(rectMark, (center[0]+offset,center[1]+offset), (bottom_right[0]-offset,bottom_right[1]-offset), (255,255,255), 1)

                rect_img1 = frame[upper_left[1]+offset : center[1]-offset, upper_left[0]+offset : center[0]-offset]
                rect_img2 = frame[upper_left[1]+offset : center[1]-offset, center[0]+offset : bottom_right[0]-offset]
                rect_img3 = frame[center[1]+offset : bottom_right[1]-offset, upper_left[0]+offset : center[0]-offset]
                rect_img4 = frame[center[1]+offset : bottom_right[1]-offset, center[0]+offset : bottom_right[0]-offset]

                Cube1 = rect_img2
                Cube2 = rect_img1
                Cube3 = rect_img4
                Cube4 = rect_img3

                global cubeCols
                cubeCols = list()
                cubeCols.append(list(cv2.split(Cube1)))
                cubeCols.append(list(cv2.split(Cube2)))
                cubeCols.append(list(cv2.split(Cube3)))
                cubeCols.append(list(cv2.split(Cube4)))
                text = side[count]

                cv2.putText(frame, 
                        'ALIGN ' + text + 'FACE',
                        (50,50),
                        font, 2,
                        (0,0,0),
                        2,
                        cv2.LINE_4)

                #show the video frame
                #cv2.imshow('frame', frame)
                #cv2.imshow("Color Output",colorFrame)
                CubeCols = {
                    'C0':[cv2.mean(cubeCols[0][0])[0], cv2.mean(cubeCols[0][1])[0], cv2.mean(cubeCols[0][2])[0]],
                    'C1':[cv2.mean(cubeCols[1][0])[0], cv2.mean(cubeCols[1][1])[0], cv2.mean(cubeCols[1][2])[0]],
                    'C2':[cv2.mean(cubeCols[2][0])[0], cv2.mean(cubeCols[2][1])[0], cv2.mean(cubeCols[2][2])[0]],
                    'C3':[cv2.mean(cubeCols[3][0])[0], cv2.mean(cubeCols[3][1])[0], cv2.mean(cubeCols[3][2])[0]]
                }

                # Preview Screen colors
                cv2.rectangle(rectMark, (upper_left[0]+offset,upper_left[1]+offset), (center[0]-offset,center[1]-offset), defaultCols[classifier.PredictColor(CubeCols['C1'][0],CubeCols['C1'][1],CubeCols['C1'][2])], -1)
                cv2.rectangle(rectMark, (center[0]+offset,upper_left[1]+offset), (bottom_right[0]-offset,center[1]-offset), defaultCols[classifier.PredictColor(CubeCols['C0'][0],CubeCols['C0'][1],CubeCols['C0'][2])], -1)
                cv2.rectangle(rectMark, (upper_left[0]+offset,center[1]+offset), (center[0]-offset,bottom_right[1]-offset), defaultCols[classifier.PredictColor(CubeCols['C3'][0],CubeCols['C3'][1],CubeCols['C3'][2])], -1)
                cv2.rectangle(rectMark, (center[0]+offset,center[1]+offset), (bottom_right[0]-offset,bottom_right[1]-offset), defaultCols[classifier.PredictColor(CubeCols['C2'][0],CubeCols['C2'][1],CubeCols['C2'][2])], -1)

                imgbytes = cv2.imencode('.png', frame)[1].tobytes()
                imgbytes2 = cv2.imencode('.png', colorFrame)[1].tobytes()
                window['Main'].update(data=imgbytes)
                window['Second'].update(data=imgbytes2)

                keypress = event

                if 'q' in keypress:
                    break

                if 'c' in event:
                    count = (count + 1) % 6
                    print(count)

                if 'x' in event:
                    count = (count - 1) % 6
                    print(count)
            
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

                if 'Return' in keypress or 'z' in keypress:
                    print('Enter pressed')
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
                        count = (count + 1) % 6

            except Exception as e:
                print("Some Error: ",str(e))

        if event == 'Exit' or event is None:
            break

        if event == 'Run Solution':
            print("Run Solution")
            cube = Solver.CubeState(PatternString(colors),'',0)
            RunnerPopup(cube)

        if event == 'Reset':
            clearColorFrame(front_up, front_down, cen_f, offset2)
            clearColorFrame(left_up, left_down, cen_l, offset2)
            clearColorFrame(right_up, right_down, cen_r, offset2)
            clearColorFrame(top_up, top_down, cen_t, offset2)
            clearColorFrame(bottom_up, bottom_down, cen_bt, offset2)
            clearColorFrame(back_up, back_down, cen_b, offset2)
            for i in range(len(colors)):
                colors[i] = [0,0,0,0]
            
    cap.release()
    cv2.destroyAllWindows()

def AlgorithmRunner(work_id, gui_queue,cube):
    status = cube.Solve()
    gui_queue.put('{} ::: done ::: {}'.format(work_id,status))
    return

def RunnerPopup(cube):

    gui_queue = queue.Queue()

    layout = [[sg.Text('Run The Bi Directional Solution Search')],
              [sg.Text('Status', size=(25, 1), key='_OUTPUT_')],
              [sg.Text(size=(25, 1), key='_OUTPUT2_')],
              [sg.Button('Go'), sg.Button('Exit')], ]

    window = sg.Window('Algorithm Runner').Layout(layout)

    work_id = 0
    while True:
        event, values = window.Read(timeout=100)

        if event is None or event == 'Exit':
            break
        if event == 'Go':
            window.Element('_OUTPUT_').Update('Starting Algorithm %s' % work_id)
            thread_id = threading.Thread(target=AlgorithmRunner, args=(work_id, gui_queue,cube,), daemon=True)
            thread_id.start()
            work_id = work_id + 1 if work_id < 19 else 0

        try:
            message = gui_queue.get_nowait()
        except queue.Empty:
            message = None

        if message is not None:
            status = str(message)
            print(status.split(":::")[2])
            window.Element('_OUTPUT2_').Update('Status %s' % status.split(":::")[2])
            work_id -= 1
            if not work_id:
                sg.PopupAnimated(None)
            
            if not('No' in (status.split(":::")[2]) or 'Incorrect' in (status.split(":::")[2])):
                print(status.split(":::")[2])
                print(status.split(":::"))
                SolutionWindow = SolutionDisplay(status.split(":::")[2],cube.state)
                SolutionWindow.DisplayWindow()

        if work_id:
            sg.PopupAnimated(sg.DEFAULT_BASE64_LOADING_GIF, background_color='white', time_between_frames=100)

    window.Close()


def PatternString(colorArray):
    pattern = list()
    scols = list()
    strPatr=""

    try:
        for side in colorArray:
            for col in side:
                scols.append(col[0])
            pattern.append(scols.copy())
            scols.clear()

        strPatr = ""
        for i in range(0,6):
            strPatr += ''.join(pattern[int(i)])
    except:
        print("Wrong Pattern")
    
    return strPatr.upper()

if __name__ == "__main__":
    classifier = KnnColor.KnnClassifier(2)
    main()
    print(colors)
    print(PatternString(colors))
    # import solution
    # SolutionWindow = SolutionDisplay("F F F F'","abcd")
    # SolutionWindow.DisplayWindow()
    


    

