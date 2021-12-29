import PySimpleGUI as sg
import CubeMoves
from tkinter import Canvas, Widget

upper_left = (300, 100)
bottom_right = (540, 340)
center = (int(((upper_left[0]+bottom_right[0])/2)),int((upper_left[1]+bottom_right[1])/2))
offset = 35
offset2 = 2

left_up = (1+20, 150)
left_down = (102+20, 250)
cen_l = (int(((left_up[0]+left_down[0])/2)),int((left_up[1]+left_down[1])/2))

front_up = (102+20, 150)
front_down = (202+20, 250)
cen_f = (int(((front_up[0]+front_down[0])/2)),int((front_up[1]+front_down[1])/2))

right_up = (202+20, 150)
right_down = (302+20, 250)
cen_r = (int(((right_up[0]+right_down[0])/2)),int((right_up[1]+right_down[1])/2))

back_up = (302+20, 150)
back_down = (404+20, 250)
cen_b = (int(((back_up[0]+back_down[0])/2)),int((back_up[1]+back_down[1])/2))

top_up = (102+20, 49)
top_down = (202+20, 150)
cen_t = (int(((top_up[0]+top_down[0])/2)),int((top_up[1]+top_down[1])/2))

bottom_up = (102+20, 250)
bottom_down = (202+20, 351)
cen_bt = (int(((bottom_up[0]+bottom_down[0])/2)),int((bottom_up[1]+bottom_down[1])/2))

Cols = {
    'B':  'Blue',
    'W':  'White',
    'R':  'Red',
    'G':  'Green',
    'Y':  'Yellow',
    'O':  'Orange',
}

moves = {
    'F':CubeMoves.Front,
    'F\'': CubeMoves.FrontP,
    'F2':CubeMoves.Front2,
    'F2\'':CubeMoves.Front2,
    'U': CubeMoves.Up,
    'U\'':CubeMoves.UpP,
    'U2': CubeMoves.Up2,
    'U2\'': CubeMoves.Up2,
    'R':CubeMoves.Right,
    'R\'': CubeMoves.RightP,
    'R2':CubeMoves.Right2,
    'R2\'':CubeMoves.Right2,
    'L': CubeMoves.Left,
    'L\'':CubeMoves.LeftP,
    'B': CubeMoves.Back,
    'B\'':CubeMoves.BackP,
    'D': CubeMoves.Down,
    'D\'':CubeMoves.DownP,
}

class SolutionDisplay:
    def __init__(self, moves, state):
        self.moves = moves
        self.state = state

    def invertMove(self,move):
        MoveInverse = {'F': 'F\'', 'F2':'F2\'', 'F2\'':'F2', 'F\'':'F',
                        'R':'R\'', 'R2':'R2\'', 'R2\'':'R2', 'R\'':'R',
                        'U':'U\'', 'U2':'U2\'', 'U2\'':'U2', 'U\'':'U',
                        'B':'B\'', 'B\'':'B',
                        'L':'L\'', 'L\'':'L',
                        'D':'D\'', 'D\'':'D'}
        return MoveInverse[move]

    def DisplayWindow(self):
        sg.theme('LightBrown1')
        layout = [
            [sg.Button('#Moves to Solve', size=(30, 2), mouseover_colors = ("grey"), key='-MOVES-', font=("Helvetica", 25))],
            [sg.Graph(canvas_size=(450, 400), graph_bottom_left=(0,400), graph_top_right=(450, 0), background_color='#97b7d8', key= 'graph')],
            [sg.T('Scroll Solution', font=("Helvetica", 20))],
            [sg.Button('< Prev',size=(6,2),font="ariel 13 bold"), sg.Button('Next >',size=(6,2),font="ariel 13 bold"), sg.Button('Exit',size=(6,2),font="ariel 13 bold")]
            ]

        window = sg.Window('SOLUTION',layout, no_titlebar=True,
                   grab_anywhere=True, finalize=True, element_justification='c')

        graph = window['graph']
        graph.DrawRectangle(bottom_up, bottom_down , line_color='purple')
        graph.DrawRectangle(top_up, top_down , line_color='purple')
        graph.DrawRectangle(right_up, right_down , line_color='purple')
        graph.DrawRectangle(left_up, left_down , line_color='purple')
        graph.DrawRectangle(front_up, front_down , line_color='Green')
        graph.DrawRectangle(back_up, back_down , line_color='purple')
        f = createCubes(front_up, front_down, cen_f, offset2, graph)
        b = createCubes(back_up, back_down, cen_b, offset2, graph)
        r = createCubes(right_up, right_down, cen_r, offset2, graph)
        l = createCubes(left_up, left_down, cen_l, offset2, graph)
        t = createCubes(top_up, top_down, cen_t, offset2, graph)
        d = createCubes(bottom_up, bottom_down, cen_bt, offset2, graph)
        count = 0
        while True:
            #try:
            event, values = window.read(timeout=0)
            window['-MOVES-'].update(self.moves)
            fillColors(self.state, graph, f,b,r,l,t,d)
            if event == sg.WIN_CLOSED:
                break
            if event == 'Exit':
                break
            if event == 'Next >':
                print("Next")
                if count >= len(self.moves.strip().split(" ")):
                    count = count
                else:
                    self.state = moves[self.moves.strip().split(" ")[count]](self.state)
                    count+=1
            if event == '< Prev':
                print("Back")
                if count <= 0:
                    count = count
                else:
                    count-=1
                    self.state = moves[self.invertMove(self.moves.strip().split(" ")[count])](self.state)
        #except Exception as e:
            #print("Close: ",count)
                #break
        window.close()

def createCubes(upper_left, bottom_right, center, offset, graph):
    cols = list()
    cols.append(graph.DrawRectangle((upper_left[0]+offset,upper_left[1]+offset), (center[0]-offset,center[1]-offset),line_color='black'))
    cols.append(graph.DrawRectangle((center[0]+offset,upper_left[1]+offset), (bottom_right[0]-offset,center[1]-offset),line_color='black'))
    cols.append(graph.DrawRectangle((upper_left[0]+offset,center[1]+offset), (center[0]-offset,bottom_right[1]-offset), line_color='black'))
    cols.append(graph.DrawRectangle((center[0]+offset,center[1]+offset), (bottom_right[0]-offset,bottom_right[1]-offset), line_color='black'))
    return cols

def fillColors(state,graph,f,b,r,l,t,d):
    # 0 to 3 = Front
    for i in range(0,4):
        graph.TKCanvas.itemconfig(f[i], fill = Cols[state[i]])
    # 4 to 7 = Right
    for i in range(0,4):
        graph.TKCanvas.itemconfig(r[i], fill = Cols[state[i+4]])
    # 7 to 11 = Back
    for i in range(0,4):
        graph.TKCanvas.itemconfig(b[i], fill = Cols[state[i+8]])
    # 11 to 15 = Left
    for i in range(0,4):
        graph.TKCanvas.itemconfig(l[i], fill = Cols[state[i+12]])
    # 15 to 19 = Back
    for i in range(0,4):
        graph.TKCanvas.itemconfig(t[i], fill = Cols[state[i+16]])
    # 19 to 23 = Down
    for i in range(0,4):
        graph.TKCanvas.itemconfig(d[i], fill = Cols[state[i+20]])


# sol = SolutionDisplay("F U B D","WWWWOOOOYYYYRRRRGGGGBBBB")
# sol.DisplayWindow()