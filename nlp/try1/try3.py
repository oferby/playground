# https://www.youtube.com/watch?v=B2q5cRJvqI8&t=1240s
# classify movie review for good/bad

import io
from wsgiref import validate

import matplotlib.pyplot as plt

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import tensorflow_datasets as tfds

WORD_COUNT = 1000
EMBEDDING_DIM = 16
EPOCHS = 3


def get_data():
    (train_data, test_data), info = tfds.load('imdb_reviews/subwords8k',
                                              split=(tfds.Split.TRAIN, tfds.Split.TEST),
                                              with_info=True,
                                              as_supervised=True
                                              )
    encoder = info.features["text"].encoder
    # print(encoder.subwords[:20])
    padded_shapes = ([None], ())

    # get training and testing batches
    train_batches = train_data.shuffle(WORD_COUNT).padded_batch(10, padded_shapes=padded_shapes)
    test_batches = train_data.shuffle(WORD_COUNT).padded_batch(10, padded_shapes=padded_shapes)
    return train_batches, test_batches, encoder


# plotting
def plot_data():
    history_dict = history.history
    acc = history_dict['accuracy']
    val_acc = history_dict['val_accuracy']
    epochs = range(1, len(acc) + 1)
    plt.figure(figsize=(6, 4))
    plt.plot(epochs, acc, 'bo', label='Training Acc')
    plt.plot(epochs, val_acc, 'b', label='Validation Acc')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.legend(loc='lower right')
    plt.ylim((0.5, 1))
    plt.show()


def get_embeddings(model, encoder):
    out_vector = io.open('/tmp/vecs.tsv', 'w', encoding='utf-8')
    out_metadata = io.open('/tmp/meta.tsv', 'w', encoding='utf-8')
    weights = model.layers[0].get_weights()[0]
    for num, word in enumerate(encoder.subwords):
        vec = weights[num + 1]
        out_metadata.write(word + '\n')
        out_vector.write('\t'.join([str(x) for x in vec]) + '\n')


def get_model():
    model = keras.Sequential(
        [
            layers.Embedding(encoder.vocab_size,
                             EMBEDDING_DIM),
            layers.GlobalAveragePooling1D(),
            layers.Dense(1, activation='sigmoid')
        ]
    )
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics='accuracy')
    return model


train_batches, test_batches, encoder = get_data()
model = get_model()

history = model.fit(train_batches, epochs=EPOCHS, validation_data=test_batches, validation_steps=20)

# plot_data()
get_embeddings(model, encoder)
