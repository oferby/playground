p = [0, 1, 0, 0, 0]
world = ['green', 'red', 'red', 'green', 'green']
measurements = ['red', 'red']
motions = [1, 1]

pHit = 0.6  # True positive
pMiss = 0.2  # False positive + False negative

# state after moves
pExact = 1
pOvershoot = 0
pUndershoot = 0


def sense(p, Z):
    q = []
    for i in range(len(p)):
        hit = (Z == world[i])
        q.append(p[i] * (hit * pHit + (1 - hit) * pMiss))
    s = sum(q)
    for i in range(len(q)):
        q[i] = q[i] / s
    return q


def move(p, U):
    q = []
    for i in range(len(p)):
        s = pExact * p[(i - U) % len(p)]
        s = s + pOvershoot * p[(i - U - 1) % len(p)]
        s = s + pUndershoot * p[(i - U + 1) % len(p)]
        q.append(s)
    return q


print("p0", p)
for k in range(len(measurements)):
    p = sense(p, measurements[k])
    print('sense', p)
    p = move(p, motions[k])
    print('move', p)

print(p)