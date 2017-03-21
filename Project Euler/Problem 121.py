# Problem 121.py
# "Disc game prize fund"
#
# Result - 2269
#
# Changelog:
# 05.01.2017 - Script created

from common import *
from fractions import Fraction

n_max = 15
n_blue = [1]

for n in range(1, 1 + n_max):
    blue_prob = Fraction(1, 1 + n)
    new_n_blue = [Fraction(0, 1)]
    for i in n_blue:
        new_n_blue[-1] += i * (1 - blue_prob)
        new_n_blue.append(i * blue_prob)
    n_blue = new_n_blue

result = int(1/sum(n_blue[-n_max//2:]))

print_result(result)
