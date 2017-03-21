# Problem 123.py
# "Prime square remainders"
#
# Result - 21035
#
# Changelog:
# 29.12.2016 - Script created

from itertools import count

result = 0

primes = [2]


def is_prime(n):
    for i in range(primes[-1] + 1, n + 1):
        for prime in primes:
            if i % prime == 0:
                break
            if prime > i**0.5:
                primes.append(i)
                break
    return n in primes

i = 0

for n in count(2):
    if is_prime(n):
        i += 1
        if (((n - 1)**i + (n + 1)**i) % (n**2)) > 10**10:
            result = i
            break

print("Result =", result)
