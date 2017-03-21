# Problem 104.py
# "Pandigital Fibonacci ends"
#
# Result - 329468
#
# Changelog:
# 23.01.2017 - Script created

from common import *
from itertools import count


def is_pandigital(x):
    if len(set(x)) != 9:
        return False
    if '0' in x:
        return False
    return True

fib_first = (int(str(Fibonacci(199))[:12]), int(str(Fibonacci(198))[:12]))
fib_last = (int(str(Fibonacci(199))[-12:]), int(str(Fibonacci(198))[-12:]))
for i in count(200):
    if i % 1000 == 0:
        print(i)
    fib_first = fib_first[0] + fib_first[1], fib_first[0]
    fib_last = fib_last[0] + fib_last[1], fib_last[0]
    if fib_first[0] > 10**12:
        fib_first = fib_first[0] / 10, fib_first[1] / 10
    if fib_last[0] > 10**12:
        fib_last = fib_last[0] % 10**12, fib_last[1] % 10**12
    if not is_pandigital(str(fib_first[0])[:9]):
        continue
    if not is_pandigital(str(fib_last[0])[-9:]):
        continue
    result = i
    break

"""for i in count():
    if i % 1000 == 0:
        print(i)
    fib = str(Fibonacci(i))
    if len(fib) < 10:
        continue
    if not is_pandigital(fib[:9]):
        continue
    if not is_pandigital(fib[-9:]):
        continue
    result = i
    break"""

print("Result =", result)
