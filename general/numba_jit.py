<<<<<<< HEAD
import numba
import random
import time


@numba.jit
def monte_carlo_pi(samples: int):
    acc = 0
    for i in range(samples):
        x = random.random()
        y = random.random()
        if (x ** 2 + y ** 2) <= 1.0:
            acc += 1
    return 4.0 * acc / samples


def monte_carlo_pi_no_numba(samples: int):
    acc = 0
    for i in range(samples):
        x = random.random()
        y = random.random()
        if (x ** 2 + y ** 2) <= 1.0:
            acc += 1
    return 4.0 * acc / samples


t1 = time.time_ns()
print(monte_carlo_pi(10000000))
t2 = time.time_ns()
print("time: ", t2 - t1)

t1 = time.time_ns()
print(monte_carlo_pi_no_numba(10000000))
t2 = time.time_ns()
print("time: ", t2 - t1)


=======
# https://neurohackademy.github.io/high-performance-python/05-numba/
from numba import jit

@jit
def fib(n):
    a, b = 1, 1
    for i in range(n):
        a, b = a+b, a
    return a


for x in range(10,20,1):
    print(fib(x))
>>>>>>> ab4510f8e2b705dbe6d130307cc165d6ecbae3af
