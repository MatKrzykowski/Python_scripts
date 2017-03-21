# Problem2.py
#
# Hubbard model with mean field approximation.
#
# Changelog:
# 16.01.2017 - Script created
# 30.01.2017 - Script refined and commented
# 17.02.2017 - Script finished

from common import *
from itertools import count  # Replacement for while loop

n = 5 #Length of the grid
n_2 = n ** 2 #Number of sited in the grid
Nstates = (n_2 - n) // 2 #Number of filled states in the grid


def main(rel_err=1E-4):
    result = []

    # Generate tight binding Hamiltonian
    H_0 = generate_TB_Hamiltonian(n)

    # Diagonalize Hamiltonian, acquire energies and eigenvectors
    energies, eigenvectors = H_0.diagonalize()

    # Acquire diagonal terms for Hubbard Hamiltonian
    diagonal = calc_diagonal(eigenvectors, Nstates)

    # Calculate total energy of states below Fermi energy
    E_total = calc_Etotal(energies, Nstates)

    # Append energies for print later
    for x in energies:
        result.append(np.array([0, x]))

    # Iteration loop
    for i in count(1):
        print(i)  # Show which iteration is running

        # Generate Hubbard Hamiltonian
        H = Hamiltonian(n_2)

        # Add TB terms with diagonal terms
        H.H = H_0.H[:, :] + np.diag(diagonal)

        # Diagonalize Hubbard Hamiltonian
        energies, eigenvectors = H.diagonalize()

        # Append new energies for output
        for x in energies:
            result.append(np.array([i, x]))

        # Calculate new diagonal terms
        diagonal = calc_diagonal(eigenvectors, Nstates)

        # Calculate new energy
        E_total_new = calc_Etotal(energies, Nstates)

        # End iteration if relative error small enough
        if 1 - rel_err < E_total / E_total_new < 1 + rel_err:
            break
        E_total = E_total_new

    # Print results to the file
    with open("Results2.txt", "w") as f:
        for i, x in result:
            f.write("{}\t{}\n".format(i, x))

    print_result(result)
    #print_charge_map(diagonal, n)

if __name__ == "__main__":
    main()
