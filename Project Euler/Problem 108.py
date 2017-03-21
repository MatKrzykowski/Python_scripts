# Problem 108.py
# "Diophantine reciprocals I"
#
# Result - 180180
#
# Changelog:
# 03.01.2017 - Script created

from common import *
from itertools import count

result = 0

def Diophantine(n):
    a = 0
    for x in range(n+1, 2*n+1):
        if (n * x) % (x - n) == 0:
            a += 1
    if n % 1000 == 0:
        print(n, a)
    return a

result = Diophantine(4*9*5*7*11*13)

print("Result =", 4*9*5*7*11*13)
