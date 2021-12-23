
# Cube will be like WWWWBBRRGGOOGGOBRRYYY
# Solved Cube is WWWWOOOOYYYYRRRRGGGGBBBB

F = {0:1, 1:3, 3:2, 2:0, 13:19, 15:18, 19:6, 18:4, 6:20, 4:21, 20:13, 21:15}
U = {16:17, 17:19, 19:18, 18:16, 0:12, 1:13, 4:0, 5:1, 8:4, 9:5, 12:8, 13:9}
R = {4:5, 5:7, 7:6, 6:4, 1:17, 3:19, 21:1, 23:3, 8:23, 10:21, 19:8, 17:10}

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

cube = 'WWWWOOOOYYYYRRRRGGGGBBBB'
# print(Front(cube))
# print(FrontP(Front(cube)))
print(Right(cube))
print(RightP(Right(cube)))