# Normal diffusion 1D.py
#
# Script calculating variance as a function of number of steps is 1D random walk
# problem (sailor problem) which is as example of descrete 1D normal diffusion.
# The expected result is for variance to be proportional to number of steps and square of step length.
# https://arxiv.org/pdf/0805.0419v1.pdf
#
# Script was written as an assignment for dr Pawlik's classes in Monte Carlo methods.
#
# Changelog:
# 27.10.2016 - Script revision

# Libraries import
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# Possible steps array: one unit to the left or to the right
possible_step = np.array([-1, 1])


def main(N=1000, k=10000, is_log_scale=True):
    """Script's main function

    N - Maximum number of steps in one simulation
    k - Number of simulations for each number of steps going from 1 to N"""

    x, y = [], []  # Declaration of arrays for plotting

    # Loop over all possible number of steps
    for n in range(1, N + 1):
        # Creating random n by k matrix of possible steps
        X = np.random.choice(possible_step, size=(n, k))
        X = np.sum(X, axis=0)  # Summing over columns leaving vector of len = k

        x.append(n)  # Append number of steps
        y.append(np.var(X))  # Append calculated variance

        print(100 * n / N, "%")  # Print the progress for logging

    # Convert to log scale if prefareable
    if is_log_scale:
        x, y = np.log(np.array(x)), np.log(np.array(y))

    # Acquire linear approximation coeficients
    a, b, *_ = stats.linregress(x, y)

    plt.plot(x, y)  # Plot variance as a function of number of steps
    plt.plot(  # Plot linear approximation, only start and end points needed
        [x[0], x[-1]],  # x coordinates
        [x[0] * a + b, x[-1] * a + b])  # y coordinates
    plt.show()  # Print the results

# Execute the script
if __name__ == "__main__":
    main()
