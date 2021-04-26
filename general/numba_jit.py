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