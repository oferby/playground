# https://arxiv.org/pdf/1605.09522.pdf

import numpy as np
import math

# X = [[2., 3.], [2.5, 4.1]]
X = [[2., 3.], [2., 3.1]]


def feature_map(x):
    return [x[0] ** 2, x[1] ** 2, x[0] * x[1] * math.sqrt(2)]

x = feature_map(X[0])
x_ = feature_map(X[1])

print(np.dot(x,x_))

x = X[0]
x_ = X[1]

print(x[0]**2 * x_[0]**2 + x[1]**2 * x_[1]**2 + 2 * x[0] * x[1] * x_[0] * x_[1])

print(np.dot(X[0],X[1])**2)

