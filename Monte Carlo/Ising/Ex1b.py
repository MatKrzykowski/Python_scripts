# Ex1b.py
#
# Exercise 1 - subpoint 2
# Observe configurations typical for low, high and critical temperatures
#
# Changelog:
# 03.12.2016 - Script created
# 05.12.2016 - Script completed

# Import from hub file
from Ising import *


def Ex1b_main(L=500, MCS=1000):
    """Module's main function

    Prints configurations for given temperatures.
    L - sidelength of the spin grid,
    MCS - number of Monte Carlo steps for each temperature.
    """

    # List of temperatures: low, critical and high
    temperatures = [0.1, Ising.critical_temp(self=None), 10]

    timer = Timer()
    n_steps_max = L**2 * MCS * len(temperatures)
    n_steps = 0

    for kT in temperatures:

        # Initialize ordered grid of size L by L and constant J = 1
        grid = Ising(L, fill_randomly=False)

        for t in range(MCS):  # Loop over time
            n_steps += L**2
            timer.print_time(n_steps / n_steps_max)
            grid.MonteCarloStep(kT)  # Monte Carlo step

        grid.output_to_file("Ex1b_" + str(kT) + ".txt", "T= " + str(kT))
        #print(grid.grid)

if __name__ == "__main__":
    Ex1b_main()  # Run the main function if script is executed
