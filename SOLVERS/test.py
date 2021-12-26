from typing import Deque
import CubeMoves
from State import State

states_for = Deque()
states_back = Deque()
solvedState = 'WWWWOOOOYYYYRRRRGGGGBBBB'
# startState = CubeMoves.randomize(solvedState)
visited_for = []
visited_back = []
childrenV_for = []
childrenV_back = []

startState = "WWWWGBGBYYYYGBGBOORROORR"
cubeMoves = ['F', 'Fp', 'R', 'Rp', 'U', 'Up']


def __main__():
    # first node from random to solved
    states_for.append(State(0, None, startState))
    state_for = states_for.popleft()

    # first node from solved to random
    states_back.append(State(0, None, solvedState))
    state_back = states_back.popleft()


    # general indexing variable
    index = 0
    
    count_1 = 0 
    count_2 = 0

    while(True):
        # if the goal state is reached
        # if(testCurrState(state)):
        #     break
        
        # state = testChildState(len(states)-6)
        # if(state != None):
        #     break


        # from random to solved state
        count_1 = addStates(childrenV_for, visited_for, states_for, moves(state_for), index, count_1)
        visited_for.append(state_for.cState)

        # from solved to random state
        count_2 = addStates(childrenV_back, visited_back, states_back, moves(states_back), index, count_2)
        visited_back.appent(state_back.cState)
        
        # index += 1
        # if(index < len(states)):
        

    # print(count)
    # displayOptimalPath(state)

def moves(state):
    return [CubeMoves.Front(state.cState),
            CubeMoves.FrontP(state.cState),
            CubeMoves.Right(state.cState),
            CubeMoves.RightP(state.cState),
            CubeMoves.Up(state.cState),
            CubeMoves.UpP(state.cState)]

def addStates(childrenV, visited, states, children, index, count):
    for ind in len(children):
        if(children[ind] in visited):
            print('State already visited')
        elif(children[ind] in childrenV):
            print('Child node already store')
        else:
            states.append(State(index, ))




def checkChildNodes():




def displayProperty(states):
    for i in states:
        print('state ', i.cState)
        print('preMove ', i.pMove)
        print('preState ', states[i.pIndex].cState)


def displayOptimalPath(state):
    print("ELLO")


def testCurrState(state):
    return state.cState == solvedState


def testChildState(startingNode):
    for startingNode in range(startingNode + 6):
        if(states[startingNode].cState == solvedState):
            return states[startingNode]
    return None


__main__()
