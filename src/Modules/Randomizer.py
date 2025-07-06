import random
import time

def GetKey():
    return time.time()

def RandomizeList(list, key):
    random.seed(key)

    tbl = list.copy()
    TblLength = len(tbl)

    for i in range(TblLength):
        NewIndex = random.randint(0, TblLength - 1)

        Old1 = tbl[i]
        Old2 = tbl[NewIndex]

        tbl[i] = Old2
        tbl[NewIndex] = Old1

    return tbl


def RandomNum(i, j, key):
    random.seed(key)

    Int = random.randint(i, j)

    return Int