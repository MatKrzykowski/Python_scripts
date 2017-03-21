# MonteCarlo.py
#
# Main script for my Monte Carlo exercises.
#
# Changelog:
# 16.12.2016 - Script created

import numpy as np
import matplotlib.pyplot as plt

is_Windows = True


class MonteCarlo_base_class:

    def __init__(self, L=10, x=[0]):
        """Initialize grid method

        x - list of possible site values,
        L - integer, length of the side of the grid.
        """
        self.grid = np.random.choice(x, size=(L, L))
        self.L = L

if __name__ == "__main__":
    print("You are not supposed to do that!")
