import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
from keras.layers import Layer, Input, Dense
from keras.models import Model
import keras.backend as K

docs = ['Well done!',
        'Good work',
        'Great effort',
        'nice work',
        'Excellent!',
        'Weak',
        'Poor effort!',
        'not good',
        'poor work',
        'Could have done better.',
        'very good',
        'very bad',
        'very nice']

more_docs = [
    'bad work',
    'very nice',
    'good',
    'poor',
    'bad',
    'work',
    'nice',
    'not nice'
]
# define class labels
labels = np.array([1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1])


class ElmoEmbeddings(Layer):
    def __init__(self, **kwargs):
        self.dimensions = 1024
        self.trainable = True
        super(ElmoEmbeddings, self).__init__(**kwargs)

    def build(self, input_shape):
        self.elmo = hub.Module("../../data/elmo", trainable=self.trainable, name='{}_module'.format(self.name))
        self.trainable_weights += K.tf.trainable_variables(scope="^{}_module/.*".format(self.name))
        super(ElmoEmbeddings, self).build(input_shape)

    def call(self, x, mask=None):
        result = self.elmo(K.squeeze(K.cast(x, tf.string), axis=1), as_dict=True, signature='default')['default']
        return result

    def compute_mask(self, inputs, mask=None):
        return K.not_equal(inputs, '--PAD--')

    def compute_output_shape(self, input_shape):
        return (input_shape[0], self.dimensions)


input_text = Input(shape=(1,), dtype=tf.string)
embedding = ElmoEmbeddings()(input_text)
dense = Dense(256, activation='relu')(embedding)
pred = Dense(1, activation='sigmoid')(dense)

model = Model(inputs=[input_text], outputs=pred)

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
model.summary()

model.fit(docs, labels, epochs=5)
