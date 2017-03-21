# common.py
#
# Assembly of common classes and functions used in programs for my
# Correlated Systems classes.
#
# Changelog:
# 16.01.2017 - Script created
# 17.02.2017 - Functions moved from other scripts

import numpy as np
import matplotlib.pyplot as plt

t = 1

class Hamiltonian:
    """Hamiltonian class"""

    def __init__(self, n=16):
        """Clas initialization.

        n - Hamiltonian dimentionality.
        """
        self.n = n
        self.H = np.zeros((n, n))

    def __getitem__(self, i):
        return self.H[i]

    def __setitem__(self, i, x):
        self.H[i] = x

    def diagonalize(self):
        """Diagonalize Hamiltonian and return eigenvalues and eigenvectors."""

        # Diagonalization
        eigenValues, eigenVectors = np.linalg.eigh(self.H)

        # Sort from highest to lowest energies
        idx = eigenValues.argsort()[::]
        eigenValues = eigenValues[idx]
        eigenVectors = eigenVectors[:, idx]

        # Fix phase problems with transition matrix
        eigenVectors = eigenVectors.transpose()
        for vector in eigenVectors:
            if vector[-1] < 0:
                vector *= -1

        return eigenValues, eigenVectors.transpose()


def calc_diagonal(eigv, Nstates):
    return np.sum(eigv[:, :Nstates]**2, axis=1)


def calc_Etotal(energies, Nstates):
    return np.sum(energies[:Nstates])


def print_result(result):
    result = np.array(result)
    plt.plot(result[:, 0], result[:, 1], '_', markersize = 50)
    lims = plt.xlim()
    plt.xlim([lims[0]-0.5, lims[1]+0.5])
    plt.xlabel("Iteracja")
    plt.ylabel("Energia")
    plt.show()


def print_charge_map(diagonal, n):
    result = []
    for i in range(n):
        result2 = []
        for j in range(n):
            result2.append(diagonal[index(i, j, n)])
        result.append(np.array(result2))
    result = np.array(result)

    # Preparing map to be printed
    plt.imshow(result, cmap='bone', interpolation='nearest')

    # Printing the result
    plt.show()

def add_hopping_term(H, t, i, j):
    H[i, j] = t
    H[j, i] = t


def generate_TB_Hamiltonian(n):
    n_2 = n ** 2
    H = Hamiltonian(n_2)

    for x in range(n_2):
        i, j = divmod(x, n)
        if i + 1 < n:
            add_hopping_term(H, t, x, index(i + 1, j, n))
        if i - 1 > -1:
            add_hopping_term(H, t, x, index(i - 1, j, n))
        if j + 1 < n:
            add_hopping_term(H, t, x, index(i, j + 1, n))
        if j - 1 > -1:
            add_hopping_term(H, t, x, index(i, j - 1, n))
    return H


def index(i, j, n):
    """Return Hamiltonian index given matrix indices."""
    return i * n + j

if __name__ == "__main__":
    print("You are not supposed to do that!")
