from tensorflow_probability import edward2 as ed
import tensorflow as tf

tf.enable_eager_execution()

normal_rv = ed.Normal(loc=0., scale=1.)
normal_rv.distribution.log_prob(1.231)

dirichlet_rv = ed.Dirichlet(concentration=tf.ones([2, 10]))

x = ed.Normal(loc=tf.zeros(10), scale=tf.ones(10))
y = 5.
print(x + y, x / y)
tf.tanh(x * y)
print(x[2])  # 3rd normal rv
