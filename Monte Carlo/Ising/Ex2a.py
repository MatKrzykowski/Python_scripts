# Ex2a.py
#
# Exercise 2 - subpoint a
# Examine magnetization, magnetic susceptibility, energy and specific heat as
# a function of temperature for various grid sizes L
#
# Changelog:
# 06.12.2016 - Script created and completed

# Import from hub file
from Ising import *


def parameters(data, L, kT):
    """Function receives list of magnetization and energy and output parameters.

    data - 2d list of magnetization module per site and energy for given kT i L,
    L - size of the grid,
    kT - temperature.
    """
    data = np.array(data).transpose()
    return [kT,
            np.average(data[0]),  # Magnetization
            np.var(data[0]) * L**2 / kT,  # Magnetic susceptibility
            np.average(data[1]) / L**2,  # Energy
            np.var(data[1]) / L**2 / kT**2  # Specific heat
            ]


def Ex2a_main(L_list=[10, 20, 50, 100], MCS=1000):
    """Module's main function.

    Output to files system parameters as function of temperature and size.
    L - sidelength of the spin grid,
    MCS - number of Monte Carlo steps for each temperature.
    """

    timer = Timer()
    n_steps = 0
    n_steps_max = 0
    for L in L_list:
        n_steps_max += L**2
    n_steps_max *= MCS * 101

    for L in L_list:  # Loop over all examined grid sizes
        result = []  # Initialize result list to study Ising model properties
        # Initialize ordered grid of size L by L and constant J = 1
        grid = Ising(L, fill_randomly=False)
        for kT in range(200, 301):  # Loop over temperatures, 50 points, step = 0.1
            kT /= 100
            temp_result = []  # Initialize result list to save grid parameters in

            for t in range(MCS):  # Loop over time
                n_steps += L**2
                timer.print_time(n_steps / n_steps_max)
                grid.MonteCarloStep(kT)  # Monte Carlo step
                temp_result.append([abs(grid.magnetization()), grid.energy()])

            result.append(parameters(temp_result, L, kT))

        output(result, "Ex2a_" + str(L) + ".txt",
               "#Temperature\tMagnetization\tMagn._susceptibility\tEnergy\tSpecific_heat")


if __name__ == "__main__":
    Ex2a_main()  # Run the main function if script is executed
