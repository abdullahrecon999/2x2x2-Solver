from collections import deque
from typing import Deque
import CubeMoves
from state import State
import numpy as np


SOLVED = 'WWWWOOOOYYYYRRRRGGGGBBBB'
SHUFFLED = 'RWYGBROBWRYOGWGOYGBOBWYR'

CUBEMOVES = ['F', 'FP', 'R', 'RP', 'Up', 'UpP', 'B', 'BP', 'L', 'LP', 'D', 'DP']

DEFUALT_STATE = State(0,'','')

# lists which will contain all the possible states of the cube
frontier_forward = []
frontier_backward = []

# lists which will save the visited state of the cube to avoid repetition
visited_forward = []
visited_backward = []

# lists which will save the visited child nodes of the cube to avoid repitition
child_forward = []
child_backward = []


# states that will contain the current state of cube
state_forward = DEFUALT_STATE
state_backward = DEFUALT_STATE



# function to add the current state to the visited arrays or the child array
def visit(array, state):

    print("\n\n=================VISIT FUNCTION======================")
    if(type(state) == State and len(array) != 0):
        print("Pstate from visit: ", array[state.pIndex].cState)
        print("state from visit: ", state.cState)
    array.append(state)


# function to check if the two states are equal 
def check(state, checkState):
    print("\n\n=================CHECK FUNCTION======================")
    print("Checking equivalence between ", state, " ", checkState)
    return state == checkState


# function to display path from the shuffled to solved state
def displayPath(path_sh, path_so):
    print("\n\n=================DISPLAY PATH FUNCTION======================")
    print("PATH SH ", path_sh)
    print("PATH SO ", path_so)
    # if(len(path_sh) != 0):
    #     print()
    #     for state in path_sh:    
    #         print("State: ", state[0], "\t Move: ", state[1], "\t Prev State: ", state[2])
    # if(len(path_so) != 0):
    #     print("PATH SO")
    #     for state in path_so:
    #         print("State: ", state[0], "\t Move: ", state[1], "\t Prev State: ", state[2])
    # print('printing path')
    while(path_so):
        state = path_so.pop()
        print("State: ", state[0], "\t Move: ", state[1], "\t Prev State: ", state[2])
    while(path_sh):
        state = path_sh.popleft()
        print("State: ", state[0], "\t Move: ", state[1], "\t Prev State: ", state[2])

# function to create the absolute path from the shuffled to solved state
def definePath(array1, array2, state1, state2):
    print("\n\n=================DEFINE PATH FUNCTION======================")

    # print('state_forward == ', state1.cState)
    # print('state_backward == ', state2.cState)
    path_sh = Deque()
    path_so = Deque()
    # state = 0
    print(len(array1), len(array2))

    # if goal has been found from shuffled to solved state
    if (len(array1) != 0 and len(array2) == 0 ):
        print('inserting based on condition 1')
        while(not check(state1.cState, SOLVED)):
            visit(path_sh, [state1.cState, state1.pMove, array1[state1.pIndex].cState])
            state1 = array1[state1.pIndex]

    # if goal has been found from solved to shuffle state
    elif (len(array2) != 0 and len(array1) == 0 ):
        print('inserting based on condition 2')
        while(not check(state2.cState, SHUFFLED)):
            visit(path_so, [state2.cState, state2.pMove, array2[state2.pIndex].cState])
            state2 = array2[state2.pIndex]
        
    # if both arrays intersect at a point 
    elif (len(array1) != 0 and len(array2) != 0 ):
        print('inserting based on condition 3')
        while(not check(state2.cState, SOLVED)):
            print("STATE 2 AFTER CHANGING ", state2.cState)
            visit(path_sh, [state2.cState, state2.pMove, array2[state2.pIndex].cState])
            state2 = array2[state2.pIndex]
        visit(path_sh, [SOLVED, 'NO MOVES', 'NONE'])
        
        while(not check(state1.cState, SHUFFLED)):
            print("STATE 1 AFTER CHANGING ", state1.cState)
            visit(path_so, [state1.cState, state1.pMove, array1[state1.pIndex].cState])
            state1 = array1[state1.pIndex]
        visit(path_so, [SHUFFLED, 'NO MOVES', 'NONE'])
    displayPath(path_sh, path_so)


# function to check the states if any of the states matches in the other frontier array
def searchFrontier(state, checkFrontier):
    print("\n\n=================SEARCH FRONTIER FUNCTION======================")
    count = 0
    found = False
    for checkState in checkFrontier:
        if(state == checkState.cState):
            found = True
            break
        count += 1
    if found:
        return count
    return 0


# function to add the child states to the arrays
def addStates(frontier, visited, childs, index, nextStates, checkFrontier):
    print("\n\n=================ADD STATES FUNCTION======================")
    print('next States: ', nextStates)
    count = 0
    for i in range (len(nextStates)):
        print("Adding next State ", nextStates[i])
        print("parent index ", index)
        print("move ", CUBEMOVES[i])
        if(nextStates[i] in visited):
            print('state already visited')
        elif(nextStates[i] in childs):
            print('state already checked')
        else:
            visit(frontier, State(index, CUBEMOVES[i], nextStates[i]))
            visit(childs, nextStates[i])
            count = searchFrontier(nextStates[i], checkFrontier)
            if(count > 0):
                # print(frontier[len(frontier)-1].cState)
                return count, frontier[len(frontier)-1]
    return count, DEFUALT_STATE



# function that will generate all the possible states from the current state
def moves(state):
    print("\n\n=================MOVES FUNCTION======================")

    return [CubeMoves.Front(state),
            CubeMoves.FrontP(state),
            CubeMoves.Right(state),
            CubeMoves.RightP(state),
            CubeMoves.Up(state),
            CubeMoves.UpP(state),
            CubeMoves.Back(state),
            CubeMoves.BackP(state),
            CubeMoves.Left(state),
            CubeMoves.LeftP(state),
            CubeMoves.Down(state),
            CubeMoves.DownP(state)
            ]


def displayFrontier(frontier, text):
    print("\n\n=================DISPLAY FRONTIER FUNCTION======================")
    print(text)
    for state in frontier:
        print(state.cState)


# runner function
def __main__():

    print("\n\n=================MAIN FUNCTION======================")

    # variable which will hold the index of the current visited node to be used 
    # assign parent state index to each child state
    global index
    index = 0

    # setting the cube state for the forward arrays i.e. from shuffled to solved state
    state_forward = State(0, 0, SHUFFLED)

    # setting the cube for the backward arrays i.e. from solved to shuffled state
    state_backward = State(0, 0, SOLVED)

    # running code to be set
    while(True):

        visit(visited_forward, state_forward.cState)
        visit(frontier_forward, state_forward)
        visit(visited_backward, state_backward.cState)
        visit(frontier_backward, state_backward)

        if(check(state_forward.cState, SOLVED)):
            print('path found from shuffled to goal state')
            definePath(frontier_forward, [], state_forward, state_backward)
            break
        elif(check(state_backward.cState, SHUFFLED)):
            definePath([], frontier_backward, state_forward, state_backward)
            print('path found from goal to shuffled state')
            break
        else:
            print('adding states for frontier_forward')
            count1, state_forward = addStates(frontier_forward, visited_forward, child_forward, index, moves(state_forward.cState), frontier_backward)
            displayFrontier(frontier_forward, 'frontier_for')
            print('count 1 == ', count1)
            if(count1 > 0):
                print('path found from one path to another 1')
                definePath(frontier_forward, frontier_backward, state_forward, frontier_backward[count1])
                break
            print('adding states for frontier_backward')
            count2, state_backward = addStates(frontier_backward, visited_backward, child_backward, index, moves(state_backward.cState), frontier_forward)
            print(state_backward.cState, 'frontier_back')
            print('count 2 == ', count2)
            displayFrontier(frontier_backward, 'frontier_back')
            if(count2 > 0):
                print('path found from one path to another 2')
                definePath(frontier_forward, frontier_backward, frontier_forward[count2], state_backward)
                break
        index += 1
        state_forward = frontier_forward[index]
        state_backward = frontier_backward[index]
            
        
__main__()


