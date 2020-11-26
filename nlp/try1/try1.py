# https://www.youtube.com/watch?v=B2q5cRJvqI8&t=1240s
# classify movie review for good/bad

import io
import matplotlib.pyplot as plt

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import tensorflow_datasets as tfds

WORD_COUNT = 1000
EMBEDDING_DIM = 16

# embbeding = layers.Embedding(WORD_COUNT, EMBEDDING_DIM)
# result = embbeding(tf.constant([1, 2, 3]))
# print(result.numpy())

(train_data, test_data), info = tfds.load('imdb_reviews/subwords8k',
                                          split=(tfds.Split.TRAIN, tfds.Split.TEST),
                                          with_info=True,
                                          as_supervised=True
                                          )
encoder = info.features["text"].encoder
print(encoder.subwords[:20])
