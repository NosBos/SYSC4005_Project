from random_number_generation import *
from generate_distributions import *
from scipy import stats
import numpy as np
np.set_printoptions(suppress=True)
seed = 45612345431

# Server 1
lam1 = 0.09654
server1_random_values = []
rand_values = generate_random_values(300, seed)
for i in range(300):
    rand = rand_values[i]
    random_distribution_value = generate_exponential_value(lam1, rand)
    server1_random_values.append(random_distribution_value)

print(server1_random_values)
data = np.array(server1_random_values)
np.savetxt('server1.csv', data, delimiter=',', fmt='%f')

# Server 2
lam2 = 0.06436
server2_random_values = []
rand_values = generate_random_values(300, seed)
for i in range(300):
    rand = rand_values[i]
    random_distribution_value = generate_exponential_value(lam2, rand)
    server2_random_values.append(random_distribution_value)

print(server2_random_values)
data = np.array(server2_random_values)
np.savetxt('server2.csv', data, delimiter=',', fmt='%f')

# Server 3
lam3 = 0.048467
server3_random_values = []
rand_values = generate_random_values(300, seed)
for i in range(300):
    rand = rand_values[i]
    random_distribution_value = generate_exponential_value(lam3, rand)
    server3_random_values.append(random_distribution_value)

print(server3_random_values)
data = np.array(server3_random_values)
np.savetxt('server3.csv', data, delimiter=',', fmt='%f')

# Work Station 1
lam4 = 4.6521
k4 = 1.02396
work1_random_values = []
rand_values = generate_random_values(300, seed)
for i in range(300):
    rand = rand_values[i]
    random_distribution_value = generate_weibull_value(lam4, k4, rand)
    work1_random_values.append(random_distribution_value)

print(work1_random_values)
data = np.array(work1_random_values)
np.savetxt('work1.csv', data, delimiter=',', fmt='%f')

# Work Station 2
lam5 = 10.6815
k5 = 0.922808
work2_random_values = []
rand_values = generate_random_values(300, seed)
for i in range(300):
    rand = rand_values[i]
    random_distribution_value = generate_weibull_value(lam5, k5, rand)
    work2_random_values.append(random_distribution_value)

print(work2_random_values)
data = np.array(work2_random_values)
np.savetxt('work2.csv', data, delimiter=',', fmt='%f')

# Work Station 3
lam6 = 0.113693
work3_random_values = []
rand_values = generate_random_values(300, seed)
for i in range(300):
    rand = rand_values[i]
    random_distribution_value = generate_exponential_value(lam6, rand)
    work3_random_values.append(random_distribution_value)

print(work3_random_values)
data = np.array(work3_random_values)
np.savetxt('work3.csv', data, delimiter=',', fmt='%f')

# Create CSV for random values
rand_values = generate_random_values(300, seed)
data = np.array(rand_values)
np.savetxt('random_values.csv', data, delimiter=',', fmt='%f')