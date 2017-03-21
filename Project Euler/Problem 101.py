# Problem 101.py
# "Optimum polynomial"
#
# Result - 37076114526
#
# Changelog:
# 21.12.2016 - Script created. Algorythm works, but is not optimal enough to generate wanted result.
# 23.12.2016 - Problem solved

import numpy as np

def fact(n):
    if n == 0:
        return 1
    return np.product(np.array([i for i in range(1, n+1)]))

def Newton(k, n):
    return fact(n) // fact(k) // fact(n-k) * (-1)**(n + k)

def f(n):
    s = 0
    for i in range(11):
        s += (-n)**i
    return s

def f_test(n):
    return n**3

u = f
result = 0
for i in range(1, 11):
    x = np.array([u(n+1) for n in range(i)], dtype = np.int64)
    y = np.zeros(i, dtype = np.int64)
    while len(x) > 1:
        z = x
        y[len(x) - 1] = np.sum( z * np.array([Newton(i, len(z)-1) for i in range(len(z))]) )
        y[len(x) - 1] = y[len(x) - 1] // fact(len(x) - 1)
        for j in range(1, len(x)+1):
            x[j-1] -= y[len(x) - 1] * j ** (len(x) - 1)
        x = x[:-1]
    else:
        y[0] = x[0]
    for j in range(i):
        result += y[j] * (i+1)**j

print(result)
