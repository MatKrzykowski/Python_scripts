# Ex1a.py
#
# Exercise 1 - subpoint 1
# Observe transitions between metastable states with magnetization +1 and -1
#
# Changelog:
# 03.12.2016 - Script created

# Import from hub file
from Ising import *


def Ex1a_main(L=8, MCS=10000, print_graph=False):
    """Module's main function

    Draws graph of magnetization as a function of time with visible transitions
    between metastable states.
    L - sidelength of the spin grid,
    MCS - number of Monte Carlo steps.
    """

    # Print time estimate
    print("Projected simulation time: " + s_to_min(MCS * L**2 // 100000))

    result = []  # Initialize results list
    # Initialize ordered grid of size L by L and constant J = 1
    grid = Ising(L)

    kT = 2.0  # Temperature is set, just below critical temperature
    for t in range(MCS):  # Loop over time
        grid.MonteCarloStep(kT)  # Monte Carlo step

        # Append temperature and average magnetization to the result list
        result.append([t, grid.magnetization()])

    output(result, 'Ex1a.txt', first_line="MCS\tMagnetization")

    if print_graph:
        graph(result)

if __name__ == "__main__":
    Ex1a_main()  # Run the main function if script is executed
