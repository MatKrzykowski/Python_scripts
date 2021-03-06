# Problem3plus.py
#
# H-F model with mean field approximation for 2 spins.
#
# Changelog:
# 17.02.2017 - Script created

from common import *
from itertools import count  # Replacement for while loop

n = 5
n_2 = n ** 2
Nstates = 2 * (n_2 - n) // 2

def main(t=1, rel_err=1E-5):
    result = []

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

    ##################################################

    # Calculate new diagonal terms
    i = 0#Nstates // 2
    diagonal = np.array(list(calc_diagonal(eigenvectors, i)) + list(calc_diagonal(eigenvectors, Nstates - i)))

    H = Hamiltonian(n_2 * 2)
    for i in range(n_2):
        for j in range(n_2):
            H[i, j] = H_0[i, j]
            H[i + n_2, j + n_2] = H_0[i, j]
    H_0 = H

    # Iteration loop
    for z in count(1):
        # Generate H-F Hamiltonian
        H = Hamiltonian(n_2 * 2)

        # Add H-F terms spin up
        H_HF = Hamiltonian(n_2 * 2)
        for a in range(n_2):
            i, j = divmod(a, n)
            for b in range(n_2):
                if a == b:
                    continue
                k, l = divmod(b, n)
                r = ((i - k) ** 2 + (j - l) ** 2)**0.5
                H_HF[a, a] += t / r * (diagonal[b + n_2] - 0.5)

        # Add H-F terms spin down
        for a in range(n_2):
            i, j = divmod(a, n)
            for b in range(n_2):
                if a == b:
                    continue
                k, l = divmod(b, n)
                r = ((i - k) ** 2 + (j - l) ** 2)**0.5
                H_HF[a + n_2, a + n_2] += t / r * (diagonal[b] - 0.5)

        H.H = H_0.H + H_HF.H

        # Diagonalize TB Hamiltonian
        energies, eigenvectors = H.diagonalize()

        # Append new energies for output
        for x in energies:
            result.append(np.array([z, x]))

        # Calculate new diagonal terms
        diagonal = calc_diagonal(eigenvectors, Nstates)

        # Calculate new energy
        E_total_new = calc_Etotal(energies, Nstates)

        print(z, E_total / E_total_new)  # Show which iteration is running

        # End iteration if relative error small enough
        if 1 - rel_err < E_total / E_total_new < 1 + rel_err:
            break
        E_total = E_total_new

    # Print results to the file
    with open("Results3.txt", "w") as f:
        for i, x in result:
            f.write("{}\t{}\n".format(i, x))

    #print_charge_map(diagonal, n)
    print_result(result)

if __name__ == "__main__":
    main()
