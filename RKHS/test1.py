import numpy as np

X = np.array([[1, 0, 2, 2.2], [1, 0, 2, 0], [1, 0, 1, 1], [0, 0, 2, 1]])
Y = np.array([[1], [2], [3], [4]])
x_ = np.array([[0, 0, 2, 2], [0, 0, 2, 2.001]])

I = np.identity(4)
Z = np.ones((4, 4))
H = I - 1 / 4 * Z


def mean_map(x):
    x = np.matrix(x)
    m = 1 / len(x)
    mm = m * (x.transpose() * np.ones((len(x), 1))).transpose()
    mm = np.array(mm).reshape(4)
    return mm


def distance(x, y):
    x_ = (x - y)
    xy = np.sqrt(x_.dot(x_))
    return xy


def gaussian_RBF_kernel(x, y):
    xy = distance(x, y)
    return np.exp(-0.5 * xy)


for xi in X:
    print(distance(x_[0], xi))

mm = mean_map(X)
print('mean map:', mm)

print('kernel 1:', gaussian_RBF_kernel(mm, x_[0]))
print('kernel 2:', gaussian_RBF_kernel(mm, x_[1]))


def covariance(x, y):
    X = np.matrix(x)
    Y = np.matrix(y)
    return 1 / len(y) * X * H * Y


print(covariance(X, Y))
