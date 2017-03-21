# Problem 134.py
# "Prime pair connection"
#
# Result - 18613426663617118
#
# Changelog:
# 12.01.2017 - Script created
# 29.01.2017 - Slight revision

from common import print_result, Primes, Timer
from itertools import count

result = 0

primes = Primes(1001000)


def prime_pair(p1, p2):
    x = p1
    a = 10**len(str(p1))
    while True:
        x += a
        if not x % p2:
            return x

timer = Timer()
for i in count(2):
    p1, p2 = primes[i], primes[i + 1]
    if not i % 10:
        timer.print_time(p1 / 1000000)
    if p1 > 1000000:  # 1000000:
        break
    result += prime_pair(p1, p2)

print_result(result)
