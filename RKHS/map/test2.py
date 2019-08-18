import numpy as np


def flatten(m):
    return np.squeeze(np.asarray(m))


def normalize(X):
    if X.ndim == 1:
        s = sum(X)
        if s == 0:
            return X
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


class State:
    def __init__(self, id):
        self.id = id
        self.obs = 0
        self.visited = 1
        self.transit_to = []


t = [[0, 2, 3, 8], [0, 4, 5, 7], [0, 1, 2, 5], [0, 2, 5, 8], [0, 1, 2, 7]]
print('history: {}\n'.format(t))

id = 0
root = State(0)
state_map = {0: root}

for i, r in enumerate(t):
    priv = root
    print('[0,0]', end='')
    for j, c in enumerate(r):
        if c == 0:
            continue
        found = False
        for t_ in priv.transit_to:
            if t_.obs == c:
                t_.visited += 1
                priv = t_
                print(' --> [{}, {}]'.format(t_.id, t_.obs), end='')
                found = True
                break
        if found:
            continue
        id += 1
        s = State(id)
        s.obs = c
        print(' --> [{}, {}]'.format(id, c), end='')
        state_map[id] = s
        priv.transit_to.append(s)
        priv = s
    print()

# print('\nThere are {} states'.format(id + 1))

# T (s` | s, a )
# Z ( o | s )

T = np.zeros((id + 1, id + 1))
Z = np.zeros((9, id + 1))
keys = state_map.keys()

for k in keys:
    s = state_map[k]
    Z[s.obs][s.id] += 1
    for t_ in s.transit_to:
        T[s.id][t_.id] += t_.visited

# print('\nT: {}'.format(T.shape))
# fprint(T)

T = normalize(T)
Z = normalize(Z)

# print('\nT: {}'.format(T.shape))
# fprint(T)
#
# print('\nZ: {}'.format(Z.shape))
# fprint(Z)

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


# get P (s` | s )
def get_pT_for_vec(s):
    p1 = s * Tm
    s_ = np.argmax(s)
    print('\nT: p ( s` | s={} ) {}\n {} \n'.format(s_, p1.shape, flatten(p1)))
    return p1


def get_pT_for_id(s):
    Pm = get_state_vector(s)
    return flatten(get_pT_for_vec(Pm))


def get_pZ(o):
    Zm = get_obs_vector(o)
    z1 = Zm * Z
    print('\nZ: p ( s | o={} ): {}\n {}\n'.format(o, z1.shape, flatten(z1)))
    return z1


def get_posterior(pT, pZ):
    p_joint = flatten(pT) * flatten(pZ)
    return normalize(p_joint)


pT = get_pT_for_id(0)
pZ = get_pZ(1)

p_joint = get_posterior(pT, pZ)
print('P(s): {}'.format(p_joint))

# next state
pT = get_pT_for_vec(p_joint)
pZ = get_pZ(2)
p_joint = get_posterior(pT, pZ)
print('P(s): {}'.format(p_joint))

# next state
pT = get_pT_for_vec(p_joint)

