import sys
import math

primes = [2, 3]
result = []

first = int(input())
second = int(input())

for i in range(4, second):
    isPrime = True
    for num in primes:
        if i < math.sqrt(num):
            break
        if i % num == 0:
            isPrime = False
            break
    if isPrime:
        primes.append(i)
        if i > first:
            result.append(i)

print(primes)
print(result)
