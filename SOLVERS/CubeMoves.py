import random as rand

# Cube will be like WWWWBBRRGGOOGGOBRRYYY
# Solved Cube is WWWWOOOOYYYYRRRRGGGGBBBB

F = {0:1, 1:3, 3:2, 2:0, 13:19, 15:18, 19:6, 18:4, 6:20, 4:21, 20:13, 21:15}
U = {16:17, 17:19, 19:18, 18:16, 0:12, 1:13, 4:0, 5:1, 8:4, 9:5, 12:8, 13:9}
R = {4:5, 5:7, 7:6, 6:4, 1:17, 3:19, 21:1, 23:3, 8:23, 10:21, 19:8, 17:10}

B = {8:9, 9:11, 11:10, 10:8, 17:12, 16:14, 12:22, 14:23, 23:5, 22:7, 5:16, 7:17}
D = {20:21, 21:23, 23:22, 22:20, 2:6, 3:7, 6:10, 7:11, 10:14, 11:15, 14:2, 15:3}
L = {13:12, 12:14, 14:15, 15:13, 0:16, 2:18, 20:0, 22:2, 16:11, 18:9, 11:20, 9:22}

def Front(pos):
    copy = list(pos)
    Fstate = list(pos)
    for i in F:
        Fstate[F[i]] = copy[i]
    return ''.join(Fstate)

def FrontP(pos):
    copy = list(pos)
    FPstate = list(pos)
    for i in F:
        FPstate[i] = copy[F[i]]
    return ''.join(FPstate)

def Up(pos):
    copy = list(pos)
    Ustate = list(pos)
    for i in U:
        Ustate[U[i]] = copy[i]
    return ''.join(Ustate)

def UpP(pos):
    copy = list(pos)
    UPstate = list(pos)
    for i in U:
        UPstate[i] = copy[U[i]]
    return ''.join(UPstate)

def Right(pos):
    copy = list(pos)
    Rstate = list(pos)
    for i in R:
        Rstate[R[i]] = copy[i]
    return ''.join(Rstate)

def RightP(pos):
    copy = list(pos)
    RPstate = list(pos)
    for i in R:
        RPstate[i] = copy[R[i]]
    return ''.join(RPstate)


def Back(pos):
    copy = list(pos)
    Bstate = list(pos)
    for i in B:
        Bstate[B[i]] = copy[i]
    return ''.join(Bstate)

def BackP(pos):
    copy = list(pos)
    BPstate = list(pos)
    for i in B:
        BPstate[i] = copy[B[i]]
    return ''.join(BPstate)

def Down(pos):
    copy = list(pos)
    Dstate = list(pos)
    for i in D:
        Dstate[D[i]] = copy[i]
    return ''.join(Dstate)

def DownP(pos):
    copy = list(pos)
    DPstate = list(pos)
    for i in D:
        DPstate[i] = copy[D[i]]
    return ''.join(DPstate)

def Left(pos):
    copy = list(pos)
    Lstate = list(pos)
    for i in L:
        Lstate[L[i]] = copy[i]
    return ''.join(Lstate)

def LeftP(pos):
    copy = list(pos)
    LPstate = list(pos)
    for i in L:
        LPstate[i] = copy[L[i]]
    return ''.join(LPstate)

def randomize(solvedState):
    randomMethod = -1
    shuffledCube = solvedState
    for i in range (6):
        randomMethod = rand.randint(0, 5)
        print(randomMethod)
        if(randomMethod == 0):
            shuffledCube = Front(shuffledCube)
        elif(randomMethod == 1):
            shuffledCube = FrontP(shuffledCube)
        elif(randomMethod == 2):
            shuffledCube = Up(shuffledCube)
        elif(randomMethod == 3):
            shuffledCube = UpP(shuffledCube)
        elif(randomMethod == 4):
            shuffledCube = Right(shuffledCube)
        else:
            shuffledCube = RightP(shuffledCube)
    return shuffledCube

# print(randomize(cube))
# # print(Front(cube))
# # print(FrontP(Front(cube)))
# print(Right(cube))
# print(Right(cube))
# print(RightP(Right((Right(cube)))))

# print(Up(cube))
# print(UpP(Up(cube)))
# print(UpP(Up(Up(cube))))

#print(Front("WWWWOOOOYYYYRRRRGGGGBBBB"))
cube = 'WWWWOOOOYYYYRRRRGGGGBBBB'
print(Left(cube))

# print(Front(cube))
# print(FrontP(Front(cube)))
#print(Right(Right('WYWYOOOOWYWYRRRRGBGBBGBG')))
#print(RightP(Right(cube)))