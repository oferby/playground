import numpy as np

import tensorflow as tf
from keras.models import Model, model_from_json, Sequential
from keras.layers import Input, Dense, Add, Multiply
from keras.optimizers import Adam
import keras.backend as K



i1 = Input(shape=(2,))
h1 = Dense(8)(i1)

i2 = Input(shape=(3,))
h2 = Dense(8)(i2)

added = Add()([h1, h2])

out = Dense(1) (added)

model = Model(input=[i1, i2], output=out)
model.compile('adam', loss='mse')

print(model.summary())

ii1 = [1,2]
ii2 = [3,4,5]

ii1 = np.reshape(ii1, (1,2))
ii2 = np.reshape(ii2, (1,3))

# ii1 = tf.reshape(ii1, (1,2))
# ii2 = tf.reshape(ii2, (1,3))

model.predict([ii1, ii2])



model.fit([ii1,ii2], [5])
