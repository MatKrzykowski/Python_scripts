# Ex2b.py
#
# Exercise 2 - subpoint b
# Examine specific heat variance as function of temperature
# using bootstrap method.
#
# Changelog:
# 12.12.2016 - Script created and completed

# Import from hub file
from Ising import *


def Ex2b_main(L=20, MCS1=20, MCS2=20):
    """Module's main function.

    Output to file specific heat variance as function of temperature.
    L - sidelength of the spin grid,
    MCS1 - number of Monte Carlo steps for to calculate SH variance.
    MCS2 - number of Monte Carlo steps for to calculate SH.
    """

    result = []  # Initialize result list to study Ising model properties
    # Initialize ordered grid of size L by L and constant J = 1
    grid = Ising(L, fill_randomly=False)
    for kT in range(1, 51):  # Loop over temperatures, 50 points, step = 0.1
        kT /= 10
        print("kT = " + str(kT))  # Print for testing
        temp_result = []  # Initialize result list to save grid parameters in

        for t in range(MCS1):  # Loop over MC step
            print("t = " + str(t))  # Print for testing
            energies = []  # Energies list to calculate specific heat
            for i in range(MCS2):  # Loop over time
                grid.MonteCarloStep(kT)  # Monte Carlo step
                # if t % 10 == 9:  # Save parameters every 100 steps
                energies.append(grid.energy())  # Append energy to the list
            # Append specific heat to the list
            temp_result.append(np.var(np.array(energies)) / L**2 / kT**2)

        temp_result = np.array(temp_result)  # Convert to numpy array
        # Append SH and its variance to the list
        result.append([kT, np.average(temp_result), np.var(temp_result)])

    # Print the output
    output(result, "Ex2b.txt", "#Temperature\tSpecific_heat\tSpecific_heat_variance")


if __name__ == "__main__":
    Ex2b_main()  # Run the main function if script is executed
