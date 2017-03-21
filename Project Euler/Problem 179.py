# Problem 179.py
# "Consecutive positive divisors"
#
# Result - 986262
#
# Changelog:
# 29.12.2016 - Script created

import numpy as np
from itertools import combinations

n_max = 10**7

n_prev = 1
i_prev = 1
n_present = 0
result = 0

primes = [2, 3, 5, 7]


def gen_primes(n):
    for i in range(primes[-1] + 2, n + 1, 2):
        i_sqrt = i ** 0.5
        for prime in primes:
            if i % prime == 0:
                break
            if prime > i_sqrt:
                primes.append(i)
                break

gen_primes(n_max)

print("Primes generated")

divisors = [[] for i in range(n_max)]
n_divisors = [0, 1]

for prime in primes:
    number = prime
    while number < n_max:
        for i in range(number - 1, n_max, number):
            divisors[i].append(prime)
        number *= prime

print("Divisors calculated")

for i in range(2, n_max):
    if i % 1000 == 0:
        print(i / 100000, "%")
    n_present = 0
    divisor = divisors[i]
    l = []
    for j in range(1, len(divisor) + 1):
        l = l + list(combinations(divisor, j))
    for j in range(len(l)):
        l[j] = np.product(np.array(list(l[j])))
    n_divisors.append(len(set(l)))

print("Number of divisors calculated")

for i in range(2, n_max):
    n_present = 0
    if n_divisors[i] == n_divisors[i - 1]:
        result += 1

print("Result =", result)
