from tensorflow_probability import edward2 as ed
import tensorflow as tf

tf.enable_eager_execution()

x = ed.Uniform(low=3, high=4)
print(x.cdf(2.5))

