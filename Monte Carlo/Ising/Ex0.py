# Ex0.py
#
# Exercise 0th
# Draw graph of magnetization as a function of temperature and find
# critical temperature
#
# Changelog:
# 02.12.2016 - Script created
# 13.12.2016 - Script rewritten using Exercise class

# Import from hub file
from Ising import *


def Ex0_main(L=20, MCS=1000, print_graph=True):
    """Module's main function

    Draws graph of magnetization as a function of temperature.
    L - sidelength of the spin grid,
    MCS - number of Monte Carlo steps.
    """
    time_estimate(L, MCS, 50)

    result = []  # Initialize results list
    # Initialize ordered grid of size L by L and constant J = 1
    grid = Ising(L)

    for kT in np.arange(0.1, 5, 0.1):  # Loop over temperatures
        temp_result = []
        for t in range(MCS):  # Loop over time
            grid.MonteCarloStep(kT)  # Monte Carlo step

            # Append temperature and average magnetization to the result list
            temp_result.append(abs(grid.magnetization()))
        result.append([kT, np.average(np.array(temp_result))])

    output(result, 'Ex0.txt', 'Temperature\tMagnetization')

    if print_graph:
        graph(result)

if __name__ == '__main__':
    Ex0_main()
