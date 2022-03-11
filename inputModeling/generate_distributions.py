import math


def generate_weibull_value(lam, k, x):
    return lam * (-1 * math.log(1-x)) ** (1/k)


def generate_exponential_value(lam, x):
    return (-math.log(1-x))/lam

