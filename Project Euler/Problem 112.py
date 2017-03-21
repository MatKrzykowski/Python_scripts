# Problem 57.py
# "Bouncy numbers"
#
# Result - 1587000
#
# Changelog:
# 05.01.2017 - Script created

from common import *
from itertools import count

def is_decreasing(i):
    i = str(i)
    for n in range(len(i)-1):
        if i[n] < i[n+1]:
            return False
    return True

def is_increasing(i):
    i = str(i)
    for n in range(len(i)-1):
        if i[n] > i[n+1]:
            return False
    return True

def is_bouncy(i):
    if is_decreasing(i):
        return False
    if is_increasing(i):
        return False
    return True

n_bouncy = 0
for i in count(1):
    if is_bouncy(i):
        n_bouncy += 1
    if n_bouncy / i == 0.99:
        result = i
        break

print_result(result)
