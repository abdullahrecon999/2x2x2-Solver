index = 0

from State import State

def testFunc(index):
    for i in range (5):
        i+=1

testFunc(index)
print(index)


a = State(0, '', '')
print(type(a) != State)