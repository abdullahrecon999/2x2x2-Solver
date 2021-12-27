import CubeMoves
import time
from collections import deque

class CubeState:

    def __init__(self, state, move, level):
        self.state = state
        self.move = move
        self.level = level

    def Actions(self,state):
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

    def invertMove(self,move):
        MoveInverse = {'F': 'F\'', 'F2':'F2\'', 'F\'':'F',
                        'R':'R\'', 'R2':'R2\'', 'R\'':'R',
                        'U':'U\'', 'U2':'U2\'', 'U\'':'U',
                        'B':'B\'', 'B\'':'B',
                        'L':'L\'', 'L\'':'L',
                        'D':'D\'', 'D\'':'D'}
        return MoveInverse[move]

    def checkCube(self,pos):
        return CubeMoves.checkCube(pos)

    def Solve(self):
        #currstate = CubeMoves.randomize('WWWWOOOOYYYYRRRRGGGGBBBB')
        currstate = self.state
        solved = 'WWWWOOOOYYYYRRRRGGGGBBBB'

        if self.checkCube(currstate):
            start = time.time()

            cube1 = CubeState(currstate,'',0)
            cube2 = CubeState(solved,'',0)

            frontier1 = deque([cube1])
            frontier2 = deque([cube2])
            visited1 = {currstate: ''}
            visited2 = {solved: ''}
            exp_lvl1,exp_lvl2 = 0,0

            while True:
                # 1st BFS from Current State to Goal
                if(len(frontier1) == 0):
                    print("No Result")
                    return False
                    
                while len(frontier1) != 0 and frontier1[0].level == exp_lvl1:
                    #state, op, lvl = frontier1.popleft()
                    cubeObj = frontier1.popleft()
                    state = cubeObj.state
                    op = cubeObj.move
                    lvl = cubeObj.level
                    print("in 1: ",state," ",op," ",lvl)

                    if (time.time()-start) >=15:
                        return "No Solution Found"

                    if state in visited2:
                        #print("Res: ",op +" "+visited2[state])
                        print("Expansion Length: ",len(visited1) + len(visited2))
                        end = time.time()
                        print(end - start)
                        return op +" "+visited2[state]

                    for child_node in self.Actions(state):
                        if child_node[0] not in visited1:
                            visited1[child_node[0]] = op+" "+child_node[1]
                            frontier1.append(CubeState(child_node[0], op +" "+ child_node[1], lvl+1))
                            #print("\t1 Childs: ",child_node[0]," ",op +" "+child_node[1])
                exp_lvl1 +=1

                # 2nd BFS from Goal State to Current State

                if(len(frontier2) == 0):
                    print("No Result")
                    return False

                while len(frontier2) !=0 and frontier2[0].level == exp_lvl2:
                    
                    cubeObj = frontier2.popleft()
                    state = cubeObj.state
                    op = cubeObj.move
                    lvl = cubeObj.level
                    print("in 2: ",state," ",op," ",lvl)

                    if (time.time()-start) >=15:
                        return "No Solution Found"

                    if state in visited1:
                        #print("Found: ",state)
                        #print("Res: ",visited1[state]+" "+op)
                        print("Expansion Length: ",len(visited1) + len(visited2))
                        end = time.time()
                        print(end - start)
                        return visited1[state]+" "+op

                    for child_node in self.Actions(state):
                        if child_node[0] not in visited2:
                            visited2[child_node[0]] = self.invertMove(child_node[1])+" "+op
                            frontier2.append(CubeState(child_node[0], self.invertMove(child_node[1])+" "+op,lvl+1))
                            #print("\t2 Childs: ",child_node[0], invertMove(child_node[1])+" "+op)
                exp_lvl2 +=1
                
        return "[!] Cube Pattern Incorrect"

def main():
    pass

if __name__ == "__main__":
    cube = CubeState('YWBYGGBGOWROBRWWOYBRROGY','',0)    
    print(cube.Solve())