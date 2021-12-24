# from _typeshed import NoneType
import CubeMoves
from State import State

states = []
solvedState = 'WWWWOOOOYYYYRRRRGGGGBBBB'
# startState = CubeMoves.randomize(solvedState)
uniqueStates = set()
startState = "WWWWGBGBYYYYGBGBOORROORR"
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
    count = 0
    while(True):
        
        # print(state.cState)
        if(testCurrState(state)):
            break
        count = addStates(moves(state), index, count)
        state = testChildState(len(states)-6)
        # state = testChildState(len(states)-3)
        if(state != None):
            break
        index += 1
        if(index < len(states)):
            state = states[index]
    
    print(count)
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


def addStates(children, index, count):
    for i in range (6):
    # for i in range (3):
        currSize = len(uniqueStates)
        uniqueStates.add(children[i])
        if(len(uniqueStates) > currSize):
            count += 1
            states.append(State(index, cubeMoves[i], children[i]))
        else:
            print(children[i])
            print("path already visited")
    return count

def testCurrState(state):
    return state.cState == solvedState


def testChildState(startingNode):
    for startingNode in range (startingNode + 6):
    # for startingNode in range (startingNode + 3):
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