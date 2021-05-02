import timeit

code = '''
def fun():
    sum = 0
    for i in range(10000):
        sum+=i
    return sum
'''

print(timeit.timeit(stmt=code))
