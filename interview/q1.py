# https://www.youtube.com/watch?v=4tYoVx0QoN0

import numpy as np


def get_valid_checks(i, j):
    checks = []
    if (i - 1) >= 0:
        checks.append((i - 1, j))
    if (i + 1) < y:
        checks.append((i + 1, j))
    if (j - 1) >= 0:
        checks.append((i, j - 1))
    if (j + 1) < x:
        checks.append((i, j + 1))
    return checks


def check_neighbors(i, j):
    if (i, j) in visited:
        return
    if m[i][j] == 1:
        visited.add((i, j))
        m1[i][j] = 1
        next_checks = get_valid_checks(i, j)
        for k, h in next_checks:
            check_neighbors(k, h)
    else:
        visited.add((i, j))


m = np.random.choice([0, 1], size=(7, 7), p=[2. / 3, 1. / 3])
x = len(m)
y = len(m[0])

m1 = np.zeros((x, y))

visited = set()
for i in range(y):
    check_neighbors(0, i)
    check_neighbors(x - 1, i)

for i in range(x):
    check_neighbors(i, 0)
    check_neighbors(i, y - 1)

print(visited)
print(m)
print(m1)
