# Ising.py
#
# Main script of Ising model exercises for Monte Carlo classes.
#
# Changelog:
# 18.11.2016 - Script created during classes
# 02.12.2016 - Script expanded during classes, Ex0 prepared
# 05.12.2016 - Moving Monte Carlo step as method of Ising class
# 13.12.2016 - Optimizations
# 16.12.2016 - Introducing MonteCarlo master script.
#
# To-do list:
# * Check if energy and total energy deltas are OK.

# Libraries import
from MonteCarlo import *
import time
import functools


class Timer:
    """Class calculating time remaining for calculations."""

    def __init__(self, exponent=1.0):
        self.t = time.time()
        self.last_t = time.time()
        self.exponent = exponent

    def time_remain(self, percent):
        t = time.time()
        dt = t - self.t
        if percent != 0:
            T = dt / percent
            return T - dt
        else:
            return 0

    def hms(self, t):
        t = int(t)
        s = t % 60
        if t >= 60:
            t = t // 60
            m = t % 60
            if t >= 60:
                t = t // 60
                h = t % 24
                if t >= 24:
                    d = t // 24
                    return"{}d {}h {}m {}s".format(d, h, m, s)
                return "{}h {}m {}s".format(h, m, s)
            return "{}m {}s".format(m, s)
        return "{}s".format(s)

    def print_time(self, percent):
        if time.time() - self.last_t > 1.0:
            self.last_t = time.time()
            percent = percent ** self.exponent
            progress_bar = int(percent * 40)
            print("(" + "█" * progress_bar +
                  "_" * (40 - progress_bar) + ")", end="\t")
            print("{}%    {} remains           ".format(
                round(percent * 100, 2), self.hms(self.time_remain(percent))), end="\r")


def output(result, filename, first_line):
    """Outputs data from result array to output file

    result - outputed, iterable data,
    filename - string, name of the file.
    """
    f = open("results/" + filename, 'w')
    f.write(first_line + "\n")
    for i in result:
        for j in i:
            f.write(str(j) + " ")
        f.write("\n")


def graph(result, x=0, y=1):
    """Function prints graph from given result 2D array"""
    # Convert result list to numpy array
    result = np.array(result).transpose()
    plt.plot(result[x], result[y])  # Prepare the graph
    plt.show()  # Print the graph


def time_estimate(L_list, MCS, n_T):
    """Function estimating calculations time.

    Return number of second we expect simulation to run.
    L_list - list of grid sizes.
    MCS - number of Monte Carlo steps per given set of parameters,
    n_T - number of investigated temperatures.
    """
    L_list = np.array(L_list)
    time = np.sum(np.power(L_list / 10, 2)) * MCS * 0.002 * n_T
    time = int(time)
    if(time > 60):
        print("Estimated simulation time: " +
              str(time // 60) + "min " + str(time % 60) + "s")
    else:
        print("Estimated simulation time: " + str(time) + "s")


def s_to_min(s):
    """Seconds to minutes function

    Function receives number of seconds and returns string in format: Xmin Ys.
    s - number of seconds
    X - number of minutes returned
    Y - number of seconds returned
    """
    s = int(s)
    if(s > 60):
        return "Estimated simulation time: " + str(s // 60) + "min " + str(s % 60) + "s"
    else:
        return "Estimated simulation time: " + str(s) + "s"


def U(L, T, m):
    """Binder cumulant function.

    L - grid size,
    T - temperature
    m - magnetization array.
    """
    m = np.array(m)
    return 1 - np.average(np.power(m, 4)) / (3 * np.average(np.power(m, 2)) ** 2)


@functools.lru_cache()
def Metropolis(x):
    return np.exp(x)


class Ising(MonteCarlo_base_class):
    """Ising model spin grid class

    Class consists of spin grid and methods simulating Ising model.
    Ising Hamiltonian: H = -J sum over neighbors s_i * s_j
    """

    # Possible spin configurations, up or down
    possible_spin = np.array([True, False])

    def __init__(self, L=10, J=1.0, fill_randomly=True):
        """Initialize grid method

        L - integer, length of the side of the grid,
        J - double, constant lying in Ising Hamiltonian
        fill_randomly - boolean, decides method of feeling the grid
        """
        if fill_randomly:  # If filled randomly
            self.grid = np.random.choice(Ising.possible_spin, size=(L, L))
        else:  # If filled unitarly, with spin up sites only
            self.grid = np.array([[True for i in range(L)] for j in range(L)])
        self.J = J
        self.L = L

    def magnetization(self):
        """Calculate grid's magnetization"""
        return 2 * np.sum(self.grid) / self.L**2 - 1

    def energy(self):
        """Calculate energy of the system"""
        L = self.L  # Easily assign L
        result = 0  # Result variable
        x = self.grid  # == '↑'  # Convert grid to boolean 2d array

        # Loop over all spins in the grid
        for i in range(L):
            for j in range(L):
                # Assume they are all the same
                result -= 4 * self.J
                # Check if they are different using XOR
                if x[i][j] ^ x[(i + 1) % L][j]:
                    result += 2 * self.J
                if x[i][j] ^ x[i - 1][j]:
                    result += 2 * self.J
                if x[i][j] ^ x[i][(j + 1) % L]:
                    result += 2 * self.J
                if x[i][j] ^ x[i][j - 1]:
                    result += 2 * self.J
        return result // 2  # Divided by 2 because interaction are counted twice

    def localenergy(self, i, j):
        """Calculate local energy in i, j point"""
        L = self.L  # Easily assign L
        result = 0  # Result variable
        result += 8 * self.J  # Assume they are all different
        # Check if they are the same
        if self.grid[i][j] == self.grid[(i + 1) % L][j]:
            result -= 4 * self.J
        if self.grid[i][j] == self.grid[i - 1][j]:
            result -= 4 * self.J
        if self.grid[i][j] == self.grid[i][(j + 1) % L]:
            result -= 4 * self.J
        if self.grid[i][j] == self.grid[i][j - 1]:
            result -= 4 * self.J
        return result

    def switch(self, i, j):
        """Switch spin in i, j point in the grid."""
        if self.grid[i][j]:  # == '↑':
            self.grid[i][j] = False  # '↓'
        else:
            self.grid[i][j] = True  # '↑'

    def MonteCarloStep(self, kT):
        """Perform one Monte Carlo step in given temperature.

        kT - temperature
        """
        for i in range(self.L):  # Loop over x grid coordinate
            for j in range(self.L):  # Loop over y grid coordinate
                # Calculate energy of the point i, j in the grid
                deltaE = -self.localenergy(i, j)
                # Metropolis algorythm - flip if preferable or random
                # chance won
                if deltaE <= 0 or np.random.rand() < Metropolis(-deltaE / kT):
                    self.switch(i, j)

    def critical_temp(self):
        """Print critical temperature for 2D Ising model."""
        return 2.269

    def output_to_screen(self):
        """Print grid onto screen"""
        if is_Windows:
            self.grid = self.grid == '↑'  # Workaround for Windows
        print(self.grid)

    def output_to_file(self, filename, first_line):
        """Output grid onto text file.

        filename - name of the output file,
        first_line - first line to be written.
        """
        if not is_Windows:  # Print properly if not on Windows
            self.grid = list(self.grid)
            for i in range(self.L):
                for j in range(self.L):
                    if self.grid[i][j]:
                        self.grid[i][j] = '↑'
                    else:
                        self.grid[i][j] = '↓'
        f = open("results/" + filename, 'w')  # Open the file
        f.write(first_line + "\n")  # Write the first line
        for i, row in enumerate(self.grid):
            for j, node in enumerate(row):
                f.write(str(i) + " " + str(j) + " " +
                        str(int(node) * 2 - 1) + "\n")
            # f.write("\n")
        f.close()

if __name__ == '__main__':
    print("You are not supposed to do that...")
