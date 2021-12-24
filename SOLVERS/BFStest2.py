import CubeMoves
from collections import deque
#from State import State

class State:
    def __init__(self, pIndex, pMove, cState):
        self.pIndex = pIndex
        self.pMove = pMove
        self.cState = cState

def main():

    frontier1 = deque()
    frontier2 = deque()
    currstate = 'RWYGBROBWRYOGWGOYGBOBWYR'
    solved = 'WWWWOOOOYYYYRRRRGGGGBBBB'
    visited1 = []
    visited2 = []

    frontier1.append(currstate)
    visited1.append(currstate)

    frontier2.append(solved)
    visited2.append(solved)

    while (len(frontier1) != 0):
        child = frontier1.popleft()
        print("Selected: ",child)

        # if (child == solved):
        #     print("State reached")
        #     break

        if (child in frontier2):
            print("State reached by 2")
            break

        # for each child of child
        for childs in moves(child):
            #print(childs," :: ",end='')
            if (childs not in visited1):
                frontier1.append(childs)
                visited1.append(childs)
            else:
                print("visited")

        # solved BFS
        child = frontier2.popleft()
        print("Selected: ",child)

        # if (child == solved):
        #     print("State reached")
        #     break

        if (child in frontier1):
            print("State reached by 1")
            break

        # for each child of child
        for childs in moves(child):
            #print(childs," :: ",end='')
            if (childs not in visited2):
                frontier2.append(childs)
                visited2.append(childs)
            else:
                print("visited")

def moves(state):
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
            CubeMoves.DownP(state)]

if __name__ == "__main__":
    main()