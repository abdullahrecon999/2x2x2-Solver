import PySimpleGUI as sg
from tkinter import Canvas
sg.theme('LightBrown1')

layout = [
    [sg.Button('#Moves to Solve', size=(30, 2), mouseover_colors = ("grey"), key='-MOVES-', font=("Helvetica", 25))],
    [sg.Canvas(size=(750, 450), background_color='#97b7d8', key= 'canvas')],
    [sg.T('Change circle color to:'), sg.Button('Red'), sg.Button('Blue')]
    ]

window = sg.Window('SOLUTION', layout, finalize=True, element_justification='c')

canvas = window['canvas']
#Canvas.create_rectangle()
#cir = list()
for i in range(0,2):
    for j in range(0,2):
        cir = canvas.TKCanvas.create_rectangle(10*(i+1),20*(i+1),30*(i+1),40*(i+1))

def showSol(moves):
    while True:
        event, values = window.read(timeout=0)
        window['-MOVES-'].update(moves)
        window.refresh()
        if event == sg.WIN_CLOSED:
            break
        if event == 'Blue':
            canvas.TKCanvas.itemconfig(cir[1], fill="Blue")
        elif event == 'Red':
            canvas.TKCanvas.itemconfig(cir, fill="Red")

showSol("F F F F")