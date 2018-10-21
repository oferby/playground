from __future__ import absolute_import, division, print_function

import tensorflow as tf

tf.enable_eager_execution()
tf.executing_eagerly()        # => True

model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Conv1D())

