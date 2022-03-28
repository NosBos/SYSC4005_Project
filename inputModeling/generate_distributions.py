try:
    from random_number_generation import *
except ImportError:
    from .random_number_generation import *
import math


def generate_weibull_value(lam, k, x):
    return lam * (-1 * math.log(1-x)) ** (1/k)


def generate_exponential_value(lam, x):
    return (-math.log(1-x))/lam


def generate_value_inspector_1(value):
    lam = 0.09654
    return generate_exponential_value(lam, value)


def generate_value_inspector_2(value):
    lam = 0.06436
    return generate_exponential_value(lam, value)


def generate_value_inspector_3(value):
    lam = 0.048467
    return generate_exponential_value(lam, value)


def generate_value_work_station_1(value):
    lam = 4.6521
    k = 1.02396
    return generate_weibull_value(lam, k, value)


def generate_value_work_station_2(value):
    lam = 10.6815
    k = 0.922808
    return generate_weibull_value(lam, k, value)


def generate_value_work_station_3(value):
    lam = 0.113693
    return generate_exponential_value(lam, value)

