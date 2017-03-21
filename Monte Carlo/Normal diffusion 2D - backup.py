# Normal diffusion 2D.py
#
# Diffusion coefficient D
# D = <delta r**2> / 4 / MCS
#
# Changelog
# 04.11.2016 - Script created
# 01.12.2016 - Script rewritten

# Libraries import
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


class atom:
    # Class defining atoms used in simulation

    # Initialize object
    def __init__(self, r):
        self.r = np.array(r)
        self.deltar = np.array([0, 0])

    # Calculate diffusion coefficient D
    def D(self, MCS):
        return np.sum(np.square(self.deltar)) / 4  # / MCS


L = 5  # Length of the 2D map
L2 = L ** 2  # Number of sites in the map
N = 1  # Number of atoms on the map
c = N / L2  # Concentration of the atoms

# np.random.seed(420) # Set seed to random function
random = np.random.randint  # Assign random function

tmax = 50000
tpercent = tmax // 100

LEFT = np.array([-1, 0])
RIGHT = np.array([1, 0])
UP = np.array([0, -1])
DOWN = np.array([0, 1])

randomstep = [LEFT, RIGHT, UP, DOWN]


def output(A, filename):
    # Output [x, y] vector for output.txt file
    f = open(filename, 'w')
    for i in A:
        f.write(str(i[0]) + " " + str(i[1]) + "\n")
    f.close()


def output2(A, filename):
    # Output [x, y] vector for output.txt file
    f = open(filename, 'w')
    for i in A:
        f.write(str(i) + "\n")
    f.close()


DofC = []
# Main loop
for N in range(1, L2):
    # N = 1
    # if(N == 1):
    c = N / L2
    print("c = " + str(c * 100) + "%")

    points = set()  # Initialize set of points

    # Generate N points
    for i in range(N):
        while True:
            A = (random(L), random(L))
            if not A in points:
                points.add(A)
                break

    items = [atom(point) for point in points]  # Generate array of atoms

    result = []  # Initialize results array

    # Loop over MCS
    for t in range(1, tmax):
        # Loop over atoms
        for item in items:
            x = 0

            deltar = randomstep[random(4)]

            r = (item.r + deltar) % L

            if not tuple(r) in points:
                points.remove(tuple(item.r))
                points.add(tuple(r))
                item.r = r
                item.deltar += deltar

            x += item.D(t)  # Add

        result.append(x / N)  # Append to result list

    DofC.append([c, np.sum(result) / tmax])  # Append calculatedD to DofC list

    # Print <r**2> / 4 for 4 cases
    if N == 1:
        output2(result, 'outputN1.txt')
    if N == 4:
        output2(result, 'outputN4.txt')
    if N == 9:
        output2(result, 'outputN9.txt')
    if N == 16:
        output2(result, 'outputN16.txt')

DofC.append([1, 0])
output(DofC, 'output.txt')  # Print D of c
