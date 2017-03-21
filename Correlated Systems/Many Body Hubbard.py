# Problem4.py
#
# Many body effects with Hubbard model.
#
# Changelog:
# 30.01.2017 - Script created

from common import Hamiltonian
from itertools import combinations
import matplotlib.pyplot as plt
import numpy as np

n = 3
n_2 = n ** 2
Nstates = 3


def index(i, j):
    """Return Hamiltonian index given matrix indices."""
    return i * n + j


def add_hopping_term(H, t, i, j):
    H[i, j] = t
    H[j, i] = t


def calc_diagonal(eigv):
    return np.sum(eigv[:, :Nstates]**2, axis=1)


def calc_Etotal(energies):
    return np.sum(energies[:Nstates])


def print_result(result):
    result = np.array(result)
    plt.plot(result[:, 0], result[:, 1], '_')
    plt.show()


def print_charge_map(diagonal):
    result = []
    for i in range(n):
        result2 = []
        for j in range(n):
            result2.append(diagonal[index(i, j)])
        result.append(np.array(result2))
    result = np.array(result)

    # Preparing map to be printed
    plt.imshow(result, cmap='bone', interpolation='nearest')

    # Printing the result
    plt.show()


def state_spin(state):
    spin = 0
    for x in state:
        if x // n_2:
            spin -= 0.5
        else:
            spin += 0.5
    return spin


def r2(i, j, k, l):
    return (i - k)**2 + (j - l)**2


def are_neighbors(x, y):
    n_same = 0
    not_samex, not_samey = None, None
    for i in x:
        if i in y:
            n_same += 1
        else:
            not_samex = i
            for j in y:
                if j not in x:
                    not_samey = j
    if n_same != Nstates - 1:
        return False
    if not not_samex // n_2 == not_samey // n_2:
        return False
    not_samex, not_samey = not_samex % n_2, not_samey % n_2
    i, j = divmod(not_samex, n)
    k, l = divmod(not_samey, n)
    if r2(i, j, k, l) == 1:
        return True
    return False

eps_T = 0.02


def logZ(energies):
    T = 0
    result = []
    for i in range(500):
        T += eps_T
        x = 0
        for E in energies:
            alpha = -1.0 * E / T
            if alpha > -100:
                x += np.exp(alpha)
        result.append(np.log(x))
    return result


def specific_heat(logZ):
    T = 0
    result = []
    for i in range(1, len(logZ) - 1):
        if not i:
            continue
        T += eps_T
        result.append(2 * T * (logZ[i + 1] - logZ[i - 1]) / eps_T + T **
                      2 * (logZ[i + 1] - 2 * logZ[i] + logZ[i - 1]) / eps_T ** 2)
    return result


def entropy(logZ):
    T = 0
    result = []
    for i in range(1, len(logZ) - 1):
        if not i:
            continue
        T += eps_T
        result.append(logZ[i] + T * (logZ[i + 1] - logZ[i - 1]) / 2 / eps_T)
    return result


def main(t=1):
    states = {x: i for i, x in enumerate(combinations(
        [j for j in range(2 * n_2)], r=Nstates))}

    H = Hamiltonian(len(states))
    for x, i in states.items():
        for y in combinations([j for j in range(2 * n_2)], r=Nstates):
            if are_neighbors(x, y):
                H[states[x], states[y]] = t
                H[states[y], states[x]] = t

    energies, eigenvalues = H.diagonalize()
    energies = energies - energies[0]

    plt.plot([i * eps_T for i in range(1, 499)], specific_heat(logZ(energies)))
    plt.show()

    plt.plot([i * eps_T for i in range(1, 499)], entropy(logZ(energies)))
    plt.show()


if __name__ == "__main__":
    main()
