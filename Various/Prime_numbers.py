# Prime numbers.py
#
# Simple script calculating list prime numbers purely for testing purposes.
#
# Changelog:
# 28.10.2016 - Script revision

# Library import
import time

t0 = time.clock()  # Script start time
t = 1  # Passed time [s]
primes = []  # List of calculated prime numbers
i = 0  # Number of calculated prime numbers
n = 2  # Number checked if is prime

# Infinite loop
while True:
    # Loop over all known primes
    for j in primes:
        # Break if divisible by any known prime
        if n % j == 0:
            break
    else:  # If not examined number is a prime
        i += 1  # Primes count up
        primes.append(n)  # Add prime to the list
        # Print for log purposes every second
        if time.clock() - t0 > t:
            print(i, n, t, 's')  # Print the results
            t = int(time.clock() - t0) + 1  # Simulation time count
    n += 1
