# Triangle.py
#
# Script calculating area of a triangle which vertices are randomly chosen
# inside unit square using Monte Carlo method.
#
# Result should be equal 11 / 144 as in equation (20) in following
# https://www.diva-portal.org/smash/get/diva2:644463/FULLTEXT01.pdf
#
# Changelog:
# 03.11.2016 - Script revision

# Libraries import
import numpy as np

random = np.random.rand  # Assigning random function

result = 0.  # Result variable
N = 100000  # Number of Monte Carlo steps
n = N // 100  # Number of steps between logging event

# Loop over number of Monte Carlo steps
for i in range(N):
    # Choose random points
    xA, xB, xC, yA, yB, yC = [random() for _ in range(6)]

    # Line equation coefficients A, B and C
    # Ax + By + C = 0
    A = (yB - yA) / (xB - xA)
    B = -1.
    C = yA - xA * A

    # Lengths of sides of the triangle a, b and c
    # a = |BC| etc.
    a = ((xC - xB)**2 + (yC - yB)**2)**0.5
    b = ((xA - xC)**2 + (yA - yC)**2)**0.5
    c = ((xA - xB)**2 + (yA - yB)**2)**0.5

    # Length of the height of the triangle
    d = abs(A * xC + B * yC + C) / ((A**2 + B**2)**0.5)

    # Area of the triangle
    P = c * d / 2.

    result += P  # Add the area to the result variable

    # Logging event
    if i % n == 0:
        print(str(i // n) + "%")

print(result / N)  # Print result divided by number of simulations
