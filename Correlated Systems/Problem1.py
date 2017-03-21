# Problem1.py
#
# Tight Binding on Lieb lattice
#
# Changelog:
# 17.01.2017 - Script created

from common import *

t = 1

H = Hamiltonian(3)
H.H[0, 2] = t
H.H[2, 0] = t
H.H[1, 2] = t
H.H[2, 1] = t
energies, eigenvectors = H.diagonalize()

print(energies, "\n\n", eigenvectors)
#print(H.H)
