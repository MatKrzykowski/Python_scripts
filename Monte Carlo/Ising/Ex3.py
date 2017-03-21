# Ex3.py
#
# Exercise 3
# Apply scalling theory to the simulation results.
# Assume beta = 0.125 and ni = 1.0
#
# Changelog:
# 12.12.2016 - Script created and completed

# Import from hub file
from Ising import *


def temp(T):
    """Function returns reduced temperature function.

    t = 1.0 - T/Tc
    """
    Tc = Ising().critical_temp()
    return 1. - T / Tc


def f1(T, L, ni):
    """X axis function used for the graph.

    T - temperature,
    L - grid size,
    ni - exponent coefficient.
    """
    return np.log(abs(temp(T)) * L ** (1 / ni))


def f2(m, L, beta, ni):
    """Y axis function used for the graph.

    m - magnetization,
    L - grid size,
    beta, ni - exponent coefficients.
    """
    return np.log(m * L**(beta / ni))


def Ex3_main(L_list=[10, 20, 50], MCS=1000, beta=0.125, ni=1.0, print_graph=False):
    """Module's main function.

    Output to file scalling theory results.
    beta, ni - critical exponents,
    L - sidelength of the spin grid,
    MCS - number of Monte Carlo steps for each temperature.
    """

    for L in L_list:
        result, result2 = [], []  # Initialize result list to study Ising model properties
        # Initialize ordered grid of size L by L and constant J = 1
        grid = Ising(L, fill_randomly=False)
        for kT in range(1, 51):  # Loop over temperatures, 50 points from 2 to 2.5
            kT = 2 + kT / 100
            print("kT = " + str(kT))  # Print for testing
            temp_result = []  # Initialize result list to save grid parameters in

            for t in range(MCS):  # Loop over MC step
                grid.MonteCarloStep(kT)  # Monte Carlo step
                temp_result.append(np.abs(grid.magnetization()))

            m = np.average(np.array(temp_result))  # Magnetization
            result.append([temp(kT), m])
            result2.append([f1(kT, L, ni), f2(m, L, beta, ni)])

        # Print the output
        output(result, "Ex3_" + str(L) + ".txt", "#1-T/Tc\tMagnetization")
        output(result2, "Ex3proper_" + str(L) + ".txt", "#x\ty")

    if print_graph:  # Print graph if requested
        graph(result2)

if __name__ == "__main__":
    Ex3_main()  # Run the main function if script is executed
