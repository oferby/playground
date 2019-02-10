import numpy as np

a = np.arange(1, 51)
a = a.reshape([5, 10])
# print(a)

m = [1, 0]
for i in range(len(a)):
    for j in range(len(a[0])):
        print(i, j, (i + m[0]) % len(a), (j + m[1]) % len(a[0]), (i - m[0]) % len(a), (j - m[1]) % len(a[0]))
