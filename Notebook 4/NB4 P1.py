from decimal import Decimal
#?Decimal # Asks for a help page on the Decimal() constructor

x = 1.0 + 2.0**(-52)

print(x)
print(Decimal(x)) # What does this do?
print(Decimal(0.1) - Decimal('0.1')) # Why does the output appear as it does?

################################

from random import random

NUM_TRIALS = 2500000

print("Native arithmetic:")
#A_native = [random() for _ in range(NUM_TRIALS)]
#B_native = [random() for _ in range(NUM_TRIALS)]
#%timeit [a+b for a, b in zip(A_native, B_native)]

print("\nDecimal package:")
# A_decimal = [Decimal(a) for a in A_native]
# B_decimal = [Decimal(b) for b in B_native]
#%timeit [a+b for a, b in zip(A_decimal, B_decimal)]

################################

a = 1.0
b = 2.**(-53) # == $\epsilon_d$ / 2.0

s1 =  a - b
t1 = s1 + b

s2 =  a + b
t2 = s2 - b

print("s1:", s1.hex())
print("t1:", t1.hex())
print("\n")
print("s2:", s2.hex())
print("t2:", t2.hex())

print("")
print(t1, "vs.", t2)
print("(t1 == t2) == {}".format(t1 == t2))

################################

import numpy as np

EPS_S = np.finfo (np.float32).eps
EPS_D = np.finfo (float).eps

print("Single-precision machine epsilon:", float(EPS_S).hex(), "~", EPS_S)
print("Double-precision machine epsilon:", float(EPS_D).hex(), "~", EPS_D)

################################

def alg_sum(x): # x == x[:n]
    s = 0.
    for x_i in x: # x_0, x_1, \ldots, x_{n-1}
        s += x_i
    return s

print("Single-precision: 1/epsilon_s ~= {:.1f} million".format(1e-6 / EPS_S))
print("Double-precision: 1/epsilon_d ~= {:.1f} quadrillion".format(1e-15 / EPS_D))

################################################################
""" 
################
# Exercise 0
'''
In the code cell below, we've defined a list,
    N = [10, 100, 1000, 10000, 100000, 1000000, 10000000]
- Take each entry N[i] to be a problem size.
- Let t[:len(N)] be a list, which will hold computed sums.
- For each N[i], run an experiment where you sum a list of values x[:N[i]] using alg_sum(). You should initialize x[:] so that all elements have the value 0.1. Store the computed sum in t[i].
'''
################

N = [10, 100, 1000, 10000, 100000, 1000000, 10000000]
# Initialize an array t of size len(N) to all zeroes.
t = [0.0] * len(N)
# Your code should do the experiment described above for
# each problem size N[i], and store the computed sum in t[i].

for index, i in enumerate(N):
    x = [0.1] * i
    t[index] = alg_sum(x)


################
# Test: `experiment_results`
#import pandas as pd
#from IPython.display import display

#import matplotlib.pyplot as plt
#%matplotlib inline

s = [1., 10., 100., 1000., 10000., 100000., 1000000.] # exact sums
t_minus_s_rel = [(t_i - s_i) / s_i for s_i, t_i in zip (s, t)]
rel_err_computed = [abs(r) for r in t_minus_s_rel]
rel_err_bound = [ni*EPS_D for ni in N]

# Plot of the relative error bound
#plt.loglog (N, rel_err_computed, 'b*', N, rel_err_bound, 'r--')

print("Relative errors in the computed result:")
#display (pd.DataFrame ({'n': N, 'rel_err': rel_err_computed, 'rel_err_bound': [n*EPS_D for n in N]}))

assert all([abs(r) <= n*EPS_D for r, n in zip(t_minus_s_rel, N)])

print("\n(Passed!)")

################################################################

def alg_dot (x, y):
    p = [xi*yi for (xi, yi) in zip (x, y)]
    s = alg_sum (p)
    return s """


################
# Exercise 1
'''
Skip!
'''
################


################################################################


################
# Exercise 2
'''
Based on the preceding observation, implement a new summation function, alg_sum_accurate(x) that computes a more accurate sum than alg_sum().
Hint 1. You do not need Decimal() in this problem. Some of you will try to use it, but it's not necessary.
Hint 2. Some of you will try to "implement" the error formula to somehow compensate for the round-off error. But that shouldn't make sense to do. (Why not? Because the formula above is a bound, not an exact formula.) Instead, the intent of this problem is to see if you can look at the formula and understand how to interpret it. That is, what does the formula tell you?
'''
################

def alg_sum_accurate(x):
    assert type(x) is list
    
    x.sort()
    s_hat = alg_sum(x)
    error = 0.0
    for index, i in enumerate(x):
        error += (len(x)-index) * abs(i)
    error *= EPS_D
    
    return s_hat - error

# Test: `alg_sum_accurate_test`
from math import exp
from numpy.random import lognormal

print("Generating non-uniform random values...")
N = [10, 10000, 10000000]
x = [lognormal(-10.0, 10.0) for _ in range(max(N))]
print("Range of input values: [{}, {}]".format(min(x), max(x)))

print("Computing the 'exact' sum. May be slow so please wait...")
x_exact = [Decimal(x_i) for x_i in x]
s_exact = [float(sum(x_exact[:n])) for n in N]
print("==>", s_exact)

print("Running alg_sum()...")
s_alg = [alg_sum(x[:n]) for n in N]
print("==>", s_alg)

print("Running alg_sum_accurate()...")
s_acc = [alg_sum_accurate(x[:n]) for n in N]
print("==>", s_acc)

print("Summary of relative errors:")
ds_alg = [abs(s_a - s_e) / s_e for s_a, s_e in zip(s_alg, s_exact)]
ds_acc = [abs(s_a - s_e) / s_e for s_a, s_e in zip(s_acc, s_exact)]
# display (pd.DataFrame ({'n': N,
#                         'rel_err(alg_sum)': ds_alg,
#                         'rel_err(alg_sum_accurate)': ds_acc}))

assert all([r_acc < r_alg for r_acc, r_alg in zip(ds_acc[1:], ds_alg[1:])]), \
       "The 'accurate' algorithm appears to be less accurate than the conventional one!"

print("\n(Passed!)")