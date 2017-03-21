# Ex4.py
#
# Exercise 4
# Find critical temperature using Binder cumulant method.
#
# Changelog:
# 13.12.2016 - Script created and completed

# Import from hub file
from Ising import *


def Ex4_main(L_list=[10, 20], MCS=10000, print_graph=False):
    """Module's main function.

    Output to file Binder cumulant calculations.
    L - sidelengths of the spin grid,
    MCS - number of Monte Carlo steps for each temperature.
    """
    #print(s_to_min(time_estimate(L_list, MCS, 50)))
    time_estimate(L_list, MCS, 50)

    for L in L_list:
        result = []  # Initialize result list to study Ising model properties
        # Initialize ordered grid of size L by L and constant J = 1
        grid = Ising(L, fill_randomly=True)
        # Loop over temperatures, 50 points from 2 to 2.5
        for kT in np.arange(2.0, 2.5, 0.01):
            print("kT = " + str(kT))  # Print for testing
            temp_result = []  # Initialize result list to save grid parameters in

            for t in range(MCS):  # Loop over MC step
                grid.MonteCarloStep(kT)  # Monte Carlo step
                temp_result.append(np.abs(grid.magnetization()))

            result.append([kT, U(L, kT, temp_result)])

        # Print the output
        output(result, "Ex4_" + str(L) + ".txt", "#1Temp\tBinder")

    if print_graph:  # Print graph if requested
        graph(result)

if __name__ == "__main__":
    Ex4_main()  # Run the main function if script is executed
