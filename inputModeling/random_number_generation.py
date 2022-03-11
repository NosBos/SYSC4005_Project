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

