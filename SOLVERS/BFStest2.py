import CubeMoves
from collections import deque
#from State import State

class State:
    def __init__(self, pIndex, pMove, cState):
        self.pIndex = pIndex
        self.pMove = pMove
        self.cState = cState

def main():
    ## This one dosent work
    count = 0
    frontier1 = deque()
    frontier2 = deque()
    currstate = 'RWYGBROBWRYOGWGOYGBOBWYR'
    #currstate = 'ORWRGGBWOWBOBWYGOYGYRYBR'
    #currstate = 'OYBYGOGBGGYRRYWOWWBOWRBR'
    #currstate = 'WOGYYGGORBBYTBRWOWRGORBW'
    solved = 'WWWWOOOOYYYYRRRRGGGGBBBB'
    #currstate = CubeMoves.randomize(solved)
    visited1 = set()
    visited2 = set()

    frontier1.append(currstate)
    visited1.add(currstate)

    frontier2.append(solved)
    visited2.add(solved)

    while (len(frontier1) != 0):
        count +=1
        print(count)
        child = frontier1.popleft()
        #print("Selected: ",child)

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
                visited1.add(childs)
            #else:
                #print("visited")

        # 2nd BFS from Solved state
        child2 = frontier2.popleft()
        #print("Selected: ",child2)

        # if (child == solved):
        #     print("State reached")
        #     break

        if (child2 in frontier1):
            print("State reached by 1")
            break

        # for each child of child
        for childs in moves(child2):
            #print(childs," :: ",end='')
            if (childs not in visited2):
                frontier2.append(childs)
                visited2.add(childs)
            #else:
            #    print("visited")

def moves(state):
    return [CubeMoves.Front(state),
            CubeMoves.FrontP(state),
            CubeMoves.Front2(state),
            CubeMoves.Right(state),
            CubeMoves.RightP(state),
            CubeMoves.Right2(state),
            CubeMoves.Up(state),
            CubeMoves.UpP(state),
            CubeMoves.Up2(state),
            CubeMoves.Back(state),
            CubeMoves.BackP(state),
            CubeMoves.Left(state),
            CubeMoves.LeftP(state),
            CubeMoves.Down(state),
            CubeMoves.DownP(state)]

def Actions(state):
    return [[CubeMoves.Front(state),'F'],
            [CubeMoves.FrontP(state),'F\''],
            [CubeMoves.Front2(state),'F2'],
            [CubeMoves.Right(state),'R'],
            [CubeMoves.RightP(state),'R\''],
            [CubeMoves.Right2(state),'R2'],
            [CubeMoves.Up(state),'U'],
            [CubeMoves.UpP(state),'U\''],
            [CubeMoves.Up2(state),'U2'],
            [CubeMoves.Back(state),'B'],
            [CubeMoves.BackP(state),'B\''],
            [CubeMoves.Left(state),'L'],
            [CubeMoves.LeftP(state),'L\''],
            [CubeMoves.Down(state),'D'],
            [CubeMoves.DownP(state),'D\'']]


def invertMove(move):
    MoveInverse = {'F': 'F\'', 'F2':'F2\'', 'F\'':'F',
                    'R':'R\'', 'R2':'R2\'', 'R\'':'R',
                    'U':'U\'', 'U2':'U2\'', 'U\'':'U',
                    'B':'B\'', 'B\'':'B',
                    'L':'L\'', 'L\'':'L',
                    'D':'D\'', 'D\'':'D'}
    return MoveInverse[move]

def BBFS():
    currstate = 'OGGORYYYRWRROBWOGGWWYBBB'
    solved = 'WWWWOOOOYYYYRRRRGGGGBBBB'
    #currstate = CubeMoves.randomize(solved)

    frontier1 = deque([(currstate, '', 0)])
    frontier2 = deque([(solved, '', 0)])
    visited1 = {currstate: ''}
    visited2 = {solved: ''}
    exp_lvl1,exp_lvl2 = 0,0

    while True:
        # 1st BFS from Current State to Goal
        if(len(frontier1) == 0):
            print("No Result")
            return False
            
        while len(frontier1) != 0 and frontier1[0][2] == exp_lvl1:
            state, op, lvl = frontier1.popleft()
            print("in 1: ",state," ",op," ",lvl)
            if state in visited2:
                print("Found: ",state)
                print("Res: ",op +" "+visited2[state])
                print("Expansion Length: ",len(visited1) + len(visited2))
                return True

            for child_node in Actions(state):
                if child_node[0] not in visited1:
                    visited1[child_node[0]] = op+" "+child_node[1]
                    frontier1.append((child_node[0], op +" "+ child_node[1], lvl+1))
                    print("\t1 Childs: ",child_node[0]," ",op +" "+child_node[1])
        exp_lvl1 +=1

        # 2nd BFS from Goal State to Current State

        if(len(frontier2) == 0):
            print("No Result")
            return False

        while len(frontier2) !=0 and frontier2[0][2] == exp_lvl2:
            state, op, lvl = frontier2.popleft()
            print("in 2: ",state," ",op," ",lvl)
            if state in visited1:
                print("Found: ",state)
                print("Res: ",visited1[state]+" "+op)
                print("Expansion Length: ",len(visited1) + len(visited2))
                return True

            for child_node in Actions(state):
                if child_node[0] not in visited2:
                    visited2[child_node[0]] = invertMove(child_node[1])+" "+op
                    frontier2.append((child_node[0], invertMove(child_node[1])+" "+op, lvl+1))
                    print("\t2 Childs: ",child_node[0], invertMove(child_node[1])+" "+op)
        exp_lvl2 +=1


if __name__ == "__main__":
    #main()
    BBFS()
    