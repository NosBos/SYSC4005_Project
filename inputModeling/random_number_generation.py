import math
import random
m = 1024
a = 691
c = 2131
# m should be a power of 2
# we will make a and c prime numbers


def linear_congruential_generator(x0):
    return (a * x0 + c) % m


def generate_random_values(n, seed):
    values = []
    x = linear_congruential_generator(seed)
    values.append(x / 1024)
    for i in range(n-1):
        x = linear_congruential_generator(x)
        values.append(x / 1024)

    return values


def auto_correlation_test(values):
    m=1
    i=0
    M = 299
    sum = 0

    for k in range(M):
        sum += values[i+k*m] * values[i+(k+1)*m]

    p = (1/(M+1)) * sum - 0.25
    print(f'row {p}')
    o = (math.sqrt(13 * M + 7)) / (12*(M+1))
    print(f'sigma {o}')
    z = p / o
    print(f'Z {z}')

# Auto Correlation Test below
# val = generate_random_values(300, 123)
# auto_correlation_test(val)


