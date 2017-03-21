# common.py
# "Counting fractions"
#
# File containing function often used in Project Euler problems.
#
# Changelog:
# 01.01.2017 - Prime number list generetor and is_prime included under Primes class
# 01.01.2017 - Number to string manipulation added
# 02.01.2017 - Testing utility for primes added
# 23.01.2017 - Fibonacci series added
# 28.01.2017 - Timer functionality added

import unittest
import functools
import time

#########
# Timer #
#########


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

#################
# Prime numbers #
#################


class Primes:
    """Class used to interact with prime numbers."""

    def __init__(self, n_max=100, print_progress=False):
        """Initialize class member.

        n_max - integer, maximal number to which primes are found.
        """
        self.primes = [2, 3]  # First two primes picked
        self.n_max = 3
        self.print_progress = print_progress
        self.gen_primes(n_max)  # Generate primes

    def __getitem__(self, i):
        return self.primes[i]

    def __iter__(self):
        """Initialize iterator."""
        self.index = -1
        return self

    def __next__(self):
        """Iterator's next step function."""
        self.index += 1
        # Return next prime if possible
        if self.index < self.length:
            return self.primes[self.index]
        # Stop iteration if not
        else:
            raise StopIteration

    @property
    def length(self):
        """Return number of primes found."""
        return len(self.primes)

    def gen_primes(self, n_max):
        """Function generating prime numbers.
        Return tuple of primes up to n_max.

        n_max - integer."""
        from itertools import count

        if self.print_progress:
            print("Begun primes generation.")
            timer = Timer(exponent=4 / 3)

        # Check if there is a need to generate new primes
        if n_max > self.n_max:
            for i in count((self.n_max // 6) * 6, 6):

                for n in (i - 1, i + 1):  # Primes can only be 6i-1 or 6i+1
                    if n <= self.n_max:
                        continue
                    if n > n_max:
                        break
                    for prime in self.primes:
                        # Not prime if prime divides it
                        if n % prime == 0:
                            break
                        # Prime if no prime below n**0.5 divides it
                        if prime > n**0.5:
                            self.primes.append(n)
                            if self.print_progress:
                                timer.print_time(i / n_max)
                            break

                if n + 1 > n_max:
                    break
            self.n_max = n_max  # Update n_max

        if self.print_progress:
            print("\nPrimes generated.")

    def is_prime(self, n):
        """Function checks if n is prime number. Returns boolean.

        n - integer.
        """
        # Return false if n <= 1
        if n <= 1:
            return False
        prime_max = round(n**0.5)
        # Generate additional primes if necessary
        if prime_max > self.n_max:
            self.gen_primes(prime_max)
        for prime in self.primes:
            # Prime if no prime below n**0.5 divides it
            if prime > prime_max:
                return True
            # Not prime if prime divides it
            if not n % prime:
                return False
        return True


class Primes_test(unittest.TestCase):
    """Class testing Primes class."""

    primes = Primes()  # Initialize Primes object

    def test_append(self):
        """Test if multiple prime generating doesn't append the same prime multiple times."""
        # Generate for every number between 2 and 100
        for i in range(2, 101):
            self.primes.gen_primes(i)
        self.assertEqual(self.primes.length, 25)
        # Generate for every number between 200 and 1000
        for i in range(200, 1001):
            self.primes.gen_primes(i)
        self.assertEqual(self.primes.length, 168)

    # Set of example number with information if it's prime of not
    known_primes = {
        (1, False),
        (2, True),
        (5, True),
        (997, True),
        (1002, False),
        (14641, False),
        (17389, True),
        (123459, False),
        (2750159, True)
    }

    def test_is_prime(self):
        """Test of is_prime method."""
        for number, value in self.known_primes:
            self.assertEqual(self.primes.is_prime(number), value)

    # List of primes
    list_primes = [2, 3, 5, 7, 11, 13, 17, 19]

    def test_iter(self):
        """Test of iteration."""
        self.assertEqual([i for i in self.primes if i < 20], self.list_primes)

#################################
# Number to string manipulation #
#################################


def digits_sum(number):
    """Function calculates and returns sum of digits of given number.

    number - integer or string of digits.
    """
    number = str(number)
    result = 0
    for digit in number:
        result += int(digit)
    return result


def is_palindrome(number):
    """Function checks if given number is palindromic, meaning the same forwards and backwards.

    number - string or integer.
    """
    number = str(number)
    for i in range(len(number)):
        if number[i] != number[-i - 1]:
            return False
    return True


def is_string_perm(i, j):
    """Checks if two strings are permutations of each other.

    i, j - strings.
    """
    if set(i) != set(j):
        return False
    for x in set(i):
        if i.count(x) != j.count(x):
            return False
    return True


def Lychrel(number):
    """Function calculates sum of a given number and it's reverse.
    Lychrel(abc) = abc + cba

    number - integer.
    """
    return number + int(str(number)[::-1])


class String_manipulation_test(unittest.TestCase):
    """Class testing string manipulation functions."""

    palindromes = (
        (1, True),
        (11, True),
        (12345654321, True),
        (123456554321, False),
        (123, False),
        (1221, True),
        (11211, True),
        (1233210, False)
    )

    def test_is_palindrome(self):
        """Test of is_palindrome function"""
        for number, value in self.palindromes:
            self.assertEqual(is_palindrome(number), value)

    Lychrel_examples = (
        (349, 1292),
        (1292, 4213),
        (4213, 7337),
        (47, 121)
    )

    def test_Lychrel(self):
        """Test of Lychrel function."""
        for number, result in self.Lychrel_examples:
            self.assertEqual(Lychrel(number), result)

    perm_examples = (
        ("11", "11", True),
        ("1292", "4213", False),
        ("1292", "9221", True),
        ("1100", "11", False),
        ("11111", "11", False)
    )

    def test_is_perm(self):
        """Test of is_string_perm function."""
        for i, j, result in self.perm_examples:
            self.assertEqual(is_string_perm(i, j), result)

######################################
# Factorial and binomial coefficient #
######################################


def fact(i):
    """Factorial function.

    i - integer.
    """
    if i == 1 or i == 0:
        return 1
    else:
        return i * fact(i - 1)


def C(n, k):
    """Binomial coefficient function of n over k.

    n, k - integers.
    """
    return fact(n) // fact(n - k) // fact(k)


class Binomial_test(unittest.TestCase):
    """Class testing binomial coefficient functions."""

    known_factorials = (
        (0, 1),
        (1, 1),
        (2, 2),
        (3, 6),
        (4, 24),
        (5, 120))

    def test_factorial(self):
        """Factorial function test."""
        for number, value in self.known_factorials:
            self.assertEqual(fact(number), value)

    known_binomials = (
        (0, 0, 1),
        (1, 1, 1),
        (2, 2, 1),
        (3, 1, 3),
        (4, 2, 6),
        (6, 3, 20))

    def test_binomial(self):
        """Binomial function test."""
        for n, k, value in self.known_binomials:
            self.assertEqual(C(n, k), value)

####################
# Totient function #
####################


def prime_fact(i, primes):
    """Function returns list of number's prime factors.

    i - integer,
    primes - Primes object.
    """
    fact = set()
    for prime in primes:
        if not i % prime:
            fact.add(prime)
            i = i // prime
            while not i % prime:
                i = i // prime
            if primes.is_prime(i):
                fact.add(i)
                break
    return list(fact)


def totient(n, primes):
    """Function returns value of Euler's totient function for a given number.

    n - integer,
    primes - Primes object.
    """
    if n == 1:
        return 1
    if primes.is_prime(n):
        return n - 1
    from itertools import combinations
    from numpy import product, array
    # primes.gen_primes(n)
    fact = prime_fact(n, primes)
    x = n
    for i in range(1, len(fact) + 1):
        for y in combinations(fact, i):
            x += n // int(product(array(y)) * (-1)**i)
    return x


class Totient_test(unittest.TestCase):
    """Class testing totient function."""

    known_totient = (
        (1, 1),
        (9, 6),
        (87109, 79180),
        (10007, 10006)
    )

    def test_totient(self):
        """Test of totient function."""
        primes = Primes()
        for number, value in self.known_totient:
            self.assertEqual(totient(number, primes), value)

#####################
# Fibonacci numbers #
#####################


@functools.lru_cache(maxsize=2**16)
def Fibonacci(n):
    if n < 3:
        return 1
    return Fibonacci(n - 1) + Fibonacci(n - 2)


class Fibonacci_test(unittest.TestCase):

    known_Fibonacci = (
        (1, 1),
        (2, 1),
        (16, 987)
    )

    def test_Fibonacci(self):
        """Test of Fibonacci function."""
        for number, value in self.known_Fibonacci:
            self.assertEqual(Fibonacci(number), value)

###########
# Various #
###########


def print_result(x):
    """Standard print result function."""
    print("\nResult = {0}".format(x))

#############
# Test runs #
#############

if __name__ == '__main__':
    unittest.main()
