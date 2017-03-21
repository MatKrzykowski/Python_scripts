# MC_pi.py
#
# Script evaluating number pi using Monte Carlo method written as an exercise during dr Pawlik classes.
#
# Changelog:
# 27.10.2016 - Script revision

# Libraries import
import numpy as np


def myRandom():
    """Returns tuple representing random point (x, y) with x, y in range (-1, 1)"""
    return (np.random.rand() * 2. - 1., np.random.rand() * 2. - 1.)


def isInCircle(x, y):
    """Checks if point (x, y) is within unit circle r = 1 and center O = [0, 0]"""
    return x**2 + y**2 < 1.


def main(n=250000):
    """Script's main function

    n - number of Monte Carlo steps, default value 100"""

    result = 0  # Variable counting random points within unit circle

    # Monte Carlo loop
    for i in range(n):
        if isInCircle(*myRandom()):  # Position check
            result += 1  # Increment result if True

    # Acquire final result by dividing number of successful checks by total
    # number of checks and multiply by area of a square
    result = result / n * 4

    # Print the result
    print("Evaluation of pi after", n,
          "Monte Carlo steps is", result)

# Execute stript
if __name__ == "__main__":
    main()
