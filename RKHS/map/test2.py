import numpy as np

t = [[0, 2, 3, 8], [0, 4, 5, 7], [0, 1, 2, 5], [0, 2, 5, 8], [0, 1, 2, 7]]


# T (s` | s, a )
# Z ( o | s )

class State:
    def __init__(self, id):
        self.id = id
        self.obs = 0
        self.transit_to = []


id = 0
root = State(0)
state_map = {}
state_map[0] = root

for i, r in enumerate(t):
    priv = root
    print('[0,0]', end='')
    for j, c in enumerate(r):
        if c == 0:
            continue
        for t_ in priv.transit_to:
            if t_.obs == c:
                priv = t_
                print(' --> [{}, {}]'.format(t_.id,t_.obs), end='')
                continue

        id += 1
        s = State(id)
        s.obs = c
        print(' --> [{}, {}]'.format(id, c), end='')
        state_map[id] = s
        priv.transit_to.append(s)
        priv = s
    print()

print('\nThere are {} states'.format(id + 1))

T = np.zeros((id + 1, id + 1))
Z = np.zeros((9, id + 1))
keys = state_map.keys()

for k in keys:
    s = state_map[k]
    Z[s.obs][s.id] += 1
    for t_ in s.transit_to:
        T[s.id][t_.id] += 1


def normalize(X):


    if X.ndim == 1:
        s = sum(X)
        X = [x / s for x in X]
        return X

    for i, r in enumerate(X):
        s = sum(r)
        if s > 0:
            X[i] = [x / s for x in r]
    return X


def fprint(X):
    for r in X:
        for c in r:
            print('{:.2f} '.format(c), end='')
        print()


T = normalize(T)

Z = normalize(Z)

print('\nT: {}'.format(T.shape))
fprint(T)

print('\nZ: {}'.format(Z.shape))
fprint(Z)

Zm = np.matrix(Z)
Tm = np.matrix(T)


def get_state_vector(s):
    p = np.zeros((id + 1))
    p[s] = 1
    return np.matrix(p)


def get_obs_vector(o):
    z = np.zeros(9)
    z[o] = 1
    return np.matrix(z)


Pm = get_state_vector(0)

p1 = Pm * Tm
print('\np ( s` | s=0 ) {}\n {} \n'.format(p1.shape, p1))

Zm = get_obs_vector(4)

z1 = Zm * Z
print('\np ( s | o=4 ): {}\n {}\n'.format(z1.shape, z1))


def flatten(m):
    return np.squeeze(np.asarray(m))


conf = flatten(p1) * flatten(z1)
print('\nconfidence:\n{}\n'.format(normalize(conf)))

