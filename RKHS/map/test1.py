import numpy as np

t = [[0, 2, 3, 8], [0, 4, 5, 7], [0, 1, 2, 5], [0, 2, 5, 8]]

T = np.zeros((9, 9))

ps = None
for r in t:
    for s in r:
        if ps is None:
            ps = s
            continue
        T[ps][s]+=1
        ps = s

for i, r in enumerate(T):
    s = sum(r)
    if s > 0 :
        T[i] = [x / s for x in r]


# print(T)

# prior
p = np.zeros(9)
p = np.diag(p)
p[0][2] = 1

Tm = np.matrix(T)
Pm = np.matrix(p)

print('\n0 2:\n', Pm * Tm)

# p = p * T
# print(p * T)

p = np.zeros(9)
p = np.diag(p)
p[2][5] = 1

print('\n2 5:\n', p * Tm)



