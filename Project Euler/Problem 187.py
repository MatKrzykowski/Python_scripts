# Problem 187.py
# "Consecutive positive divisors"
#
# Result - 17427258
#
# Changelog:
# 29.12.2016 - Script created
# 30.12.2016 - Script completed, after long strugles


n_max = 10**8
result = 0

primes = [2, 3, 5, 7]


def gen_primes(n):
    percent = 10**6
    for i in range(primes[-1] + 2, n + 1, 2):
        if i > percent:
            percent += 10**6
            print(i // 10**6, "%")
        i_sqrt = i ** 0.5
        for prime in primes:
            if i % prime == 0:
                break
            if prime > i_sqrt:
                primes.append(i)
                break

gen_primes(n_max)

print("Primes generated")

semiprimes = set()

percent = 10**4
for prime in primes:
    if prime >= percent:
        percent += 10**4
        print(prime / 10**6, "%")
    for prime2 in primes:
        if prime * prime2 > n_max:
            break
        if prime > prime2:
            continue
        semiprimes.add(prime * prime2)


result = len(semiprimes)
print("Result =", result)
