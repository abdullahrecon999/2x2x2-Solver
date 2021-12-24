# from _typeshed import NoneType
import CubeMoves
from State import State

states = []
solvedState = 'WWWWOOOOYYYYRRRRGGGGBBBB'
startState = CubeMoves.randomize(solvedState)
cubeMoves = [
    'F',\
    'Fp',\
    'R',\
    'Rp',
    'U',\
    'Up'
]


def __main__():
    state = State(0, None, startState)
    states.append(state)
    index = 0
    while(True):
        
        print(state.cState)
        if(testCurrState(state)):
            break
        addStates(moves(state), index)
        state = testChildState(len(states)-6)
        if(state != None):
            break
        index += 1
        state = states[index]


    displayOptimalPath(state)


def displayOptimalPath(state):
    path = []
    while(state.cState != startState):
        path.append([state.pMove, states[state.pIndex].cState])
        state = states[state.pIndex]
    print(path)

def moves(state):
    return [CubeMoves.Front(state.cState),
            CubeMoves.FrontP(state.cState),
            CubeMoves.Right(state.cState),
            CubeMoves.RightP(state.cState),
            CubeMoves.Up(state.cState),
            CubeMoves.UpP(state.cState)]


def addStates(children, index):
    for i in range (6):
        states.append(State(index, cubeMoves[i], children[i]))


def testCurrState(state):
    return state.cState == solvedState


def testChildState(startingNode):
    for startingNode in range (startingNode + 6):
        if(states[startingNode].cState == solvedState):
            return states[startingNode]
    return None

__main__()

# call all the moves and return the states to the caller method




# print(CubeMoves.Front(state.cState))
    # print(CubeMoves.FrontP(state.cState))
    # print(CubeMoves.Right(state.cState))
    # print(CubeMoves.RightP(state.cState))
    # print(CubeMoves.Up(state.cState))
    # print(CubeMoves.UpP(state.cState))

    # print('---------------------------')
    # for child in states:
    #     print(child.cState)