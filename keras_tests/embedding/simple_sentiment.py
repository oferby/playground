import os.path

import keras.preprocessing.sequence as S
import keras.preprocessing.text as T
import numpy as np
from keras.layers import Embedding, Dense, Flatten,LSTM,TimeDistributed,RepeatVector
from keras.models import Sequential
from keras.models import model_from_json

# https://machinelearningmastery.com/use-word-embedding-layers-deep-learning-keras/

# tf.enable_eager_execution()
vocab_size = 50
max_length = 4
NUMPY_FILE_NAME = 'padded_docs.npy'


def create_or_load_padded_docs():
    docs = ['Well done!',
            'Good work',
            'Great effort',
            'nice work',
            'Excellent!',
            'Weak',
            'Poor effort!',
            'not good',
            'poor work',
            'Could have done better.']

    labels = np.array([1, 1, 1, 1, 1, 0, 0, 0, 0, 0])

    if os.path.isfile(NUMPY_FILE_NAME):
        padded_docs = np.load(NUMPY_FILE_NAME)
    else:
        # integer encode the documents
        encoded_docs = [T.one_hot(d, vocab_size) for d in docs]
        # pad documents to a max length of 4 words
        padded_docs = S.pad_sequences(encoded_docs, maxlen=max_length, padding='post')
        np.save(NUMPY_FILE_NAME, padded_docs)

    print('padded docs:', padded_docs)
    return padded_docs, labels


def create_model():
    model = Sequential()
    model.add(Embedding(vocab_size, 8, input_length=max_length))
    model.add(Flatten())
    model.add(Dense(1, activation='sigmoid'))
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['acc'])
    print(model.summary())

    # fit the model
    model.fit(padded_docs, labels, epochs=300, verbose=1)

    # serialize model to JSON
    model_json = model.to_json()
    with open("model.json", "w") as json_file:
        json_file.write(model_json)
    # serialize weights to HDF5
    model.save_weights("model.h5")
    print("Saved model to disk")
    return model


def load_model():
    # load json and create model
    json_file = open('model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights("model.h5")
    loaded_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['acc'])
    print("Loaded model from disk")
    return loaded_model


padded_docs, labels = create_or_load_padded_docs()

model = None
if os.path.isfile('model.json'):
    model = load_model()
else:
    model = create_model()

# evaluate
loss, accuracy = model.evaluate(padded_docs, labels, verbose=0)
print('Accuracy:', accuracy, 'Loss:', loss)
