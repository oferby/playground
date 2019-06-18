# coin toss

import numpy as np
import tensorflow as tf

tf.enable_eager_execution()

X = np.asarray([0, 2, 3, 1])
P = np.asarray([.1, .3, .4, .2])


def k(x, y):
    # k(x,y) = (x-y)^2 when holding y constant
    return (x - y) ** 2


# get probability of x
def f(x):
    depth = len(X)
    return tf.one_hot(X, depth)


# run feature map
def fee(x):
    fi = []
    for i in range(len(X)):
        fi.append(P[i] * k(x, X[i]))
    return np.asarray(fi)


# print(np.dot(f(0), mu()))

mu = np.zeros(len(X))
for i in range(len(X)):
    mu += fee(X[i]) * P[i]

print(mu)

# print(np.dot(f(1), mu))
