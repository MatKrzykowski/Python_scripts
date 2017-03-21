# Problem4.py
#
# Many body H-F model with mean field approximation.
#
# Changelog:
# 17.02.2017 - Script created

from common import *
from itertools import count, permutations  # Replacement for while loop

n = 2
n_2 = 8
Nbodies = 3

def gen_permutations(x, y, perm, perms):
    if y == 0:
        perms.append(tuple(perm))
    if x > 0 and y > 0:
        gen_permutations(x-1, y-1, perm[:] + [True], perms)
    if y > x and y > 0:
        gen_permutations(x, y-1, perm[:] + [False], perms)

def many_body_TB_Hamiltonian(Nstates, states, perm_to_index):
    H = Hamiltonian(Nstates)

    for state in states:
        #Spins up
        for i in range(4):
            if not state[i]:
                continue
            for j in range(4):
                if i == j:
                    continue
                if state[j]:
                    continue
                new_state = list(state)
                new_state[i] = False
                new_state[j] = True
                a, b = perm_to_index[state], perm_to_index[tuple(new_state)]
                H.H[a, b] += 0.5
                H.H[b, a] += 0.5

        #Spins down
        for i in range(4, 8):
            if not state[i]:
                continue
            for j in range(4, 8):
                if i == j:
                    continue
                if state[j]:
                    continue
                new_state = list(state)
                new_state[i] = False
                new_state[j] = True
                a, b = perm_to_index[state], perm_to_index[tuple(new_state)]
                H.H[a, b] += 0.5
                H.H[b, a] += 0.5

    return H

def state_spin(state):
    result = 0.0
    for i in range(4):
        if state[i]:
            result += 0.5
    for i in range(4, 8):
        if state[i]:
            result -= 0.5
    return result

def main():
    #Generate permutations
    my_permutations = []
    gen_permutations(Nbodies, n_2, [], my_permutations)
    my_permutations = [i for i in my_permutations if state_spin(i) == 0.5]

    #Generate permutations dictionaries
    index_to_perm = {i: p for i, p in enumerate(my_permutations)}
    perm_to_index = {p: i for i, p in enumerate(my_permutations)}

    Nstates = len(my_permutations)

    # Generate many body TB Hamiltonian
    H_0 = many_body_TB_Hamiltonian(Nstates, my_permutations, perm_to_index)

    # Diagonalize Hamiltonian, acquire energies and eigenvectors
    energies, eigenvectors = H_0.diagonalize()

    print_result(list(zip(len(energies)*[0], energies)))
    print(energies)

if __name__ == "__main__":
    main()
