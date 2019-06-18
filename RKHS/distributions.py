import numpy as np

p0 = [.4, .1, .3, .2]
p = [[.8, .1, .05, .05], [.2, .7, .05, .05], [.05, .05, .85, .05], [.4, .2, .3, .1]]

X = []
P = {}


def sample():
    x = np.argmax(np.random.multinomial(1, p0))
    s = [x]
    for j in range(3):
        x = np.argmax(np.random.multinomial(1, p[x]))
        s.append(x)
    return s


samples = 5000
for i in range(samples):
    s = sample()
    st = str(s)
    # print(s)
    if st not in P:
        P[st] = 1
    else:
        P[st] += 1
    X.append(s)

print(P)
PL = sorted(P.keys())
print(PL)
E = []
for pl in PL:
    E.append(P[pl] / samples)

print('E: ', E, '\nlen: ', len(E), '\ntotal: ', sum(E))

x_ = []
for i in range(4):
    x_.append(np.average(np.asanyarray(X)[:, i]))

print('x`: ', x_)

print('RKHS: ', np.dot([1, 0, 0, 0], p0))

