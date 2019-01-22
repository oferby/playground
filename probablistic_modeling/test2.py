import numpy as np
import tensorflow_probability as tfp
import tensorflow as tf

tfd = tfp.distributions

tf.enable_eager_execution()

# Define a single scalar Normal distribution.
dist = tfd.Normal(loc=0., scale=3.)

# Evaluate the cdf at 1, returning a scalar.
dist.cdf(1.)

# Define a batch of two scalar valued Normals.
# The first has mean 1 and standard deviation 11, the second 2 and 22.
dist = tfd.Normal(loc=[1, 2.], scale=[11, 22.])

# Evaluate the pdf of the first distribution on 0, and the second on 1.5,
# returning a length two tensor.
dist.prob([0, 1.5])

# Get 3 samples, returning a 3 x 2 tensor.
# print(dist.sample([3]))


x_train = np.linspace(-3, 3, num=10)
x_train = x_train.astype(np.float32).reshape((1, 10))
x = tf.cast(x_train, dtype=tf.float32)
W_0 = tfd.Normal(loc=tf.zeros([10]), scale=tf.ones([10]))
b_0 = tfd.Normal(loc=tf.zeros(10), scale=tf.ones(10))

# print(W_0.sample(50))
print(W_0)
h_0 = tf.matmul(x, W_0.sample(1))
print(h_0)
# h_0 += b_0
# print(h_0)
