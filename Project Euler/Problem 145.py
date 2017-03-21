# Problem 145.py
# "How many reversible numbers are there below one-billion?"
#
# Result - 608720
#
# Changelog:
# 22.01.2017 - Script created

from common import *

result = 0

def is_reversible(i):
    if i[-1] == '0':
        return False
    leading_1 = False
    for x, y in zip(i, i[::-1]):
        z = int(x) + int(y)
        if leading_1 and z%2 == 1:
            return False
        if not leading_1 and z%2 == 0:
            return False
        leading_1 = z > 9
    return True

for i in range(1, 10**9):
    if i%10**6 == 0:
        print("{}%".format(i/10**7))
    if is_reversible(str(i)):
        result += 1


print_result(result)
