import os.path

import keras.preprocessing.sequence as S
import keras.preprocessing.text as T
import keras.utils as U
import numpy as np
from keras.layers import Embedding, Dense, LSTM
from keras.models import Sequential
from keras.models import model_from_json
import json

max_length = 4
TOKENIZER_FILE_NAME = 'simple-with-lstm-tokenizer.json'
MODEL_FILENAME = "simple-with-lstm-model.json"
WEIGHTS_FILENAME = "simple-with-lstm-weights.h5"


def create_or_load_padded_docs():
    docs = [
            'it is just fine',
            'Well done!',
            'Good work',
            'Great effort',
            'nice work',
            'Excellent!',
            'Weak',
            'Poor effort!',
            'not good',
            'poor work',
            'Could have done better.',
            'fine',
            'ok']

    labels = np.array([2, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 2, 2])
    labels = U.to_categorical(labels)

    if os.path.isfile(TOKENIZER_FILE_NAME):
        json_file = open(TOKENIZER_FILE_NAME, 'r')
        json_data = json_file.read()
        json_file.close()
        t = T.text.tokenizer_from_json(json_data)
    else:
        t = T.Tokenizer()
        t.fit_on_texts(docs)

        json_file = open(TOKENIZER_FILE_NAME, 'w')
        json_file.write(t.to_json())
        json_file.close()

    vocab_size = len(t.word_index) + 1

    sec = t.texts_to_sequences(docs)
    padded = S.pad_sequences(sec, maxlen=max_length)
    return padded, labels, vocab_size, t


def get_padded_vector(text):
    sec = t.texts_to_sequences([text])
    return S.pad_sequences(sec, maxlen=max_length)


def create_model():
    model = Sequential()
    model.add(Embedding(vocab_size, 8, input_length=max_length))
    model.add(LSTM(100))
    model.add(Dense(3, activation='sigmoid'))
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['acc'])
    print(model.summary())

    # fit the model
    print('training the model...')
    model.fit(padded, labels, epochs=200, verbose=0)

    # evaluate
    loss, accuracy = model.evaluate(padded, labels, verbose=0)
    print('Accuracy:', accuracy, 'Loss:', loss)

    # serialize model to JSON
    model_json = model.to_json()
    with open(MODEL_FILENAME, "w") as json_file:
        json_file.write(model_json)
    # serialize weights to HDF5
    model.save_weights(WEIGHTS_FILENAME)
    print("Saved model to disk")
    return model


def load_model():
    # load json and create model
    json_file = open(MODEL_FILENAME, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights(WEIGHTS_FILENAME)
    loaded_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['acc'])
    print("Loaded model from disk")
    return loaded_model


padded, labels, vocab_size, t = create_or_load_padded_docs()

model = None
if os.path.isfile(MODEL_FILENAME):
    model = load_model()
else:
    model = create_model()

x = get_padded_vector('weak effort')
y = model.predict_classes(x)
print('weak:', y)

x = get_padded_vector('nice effort')
y = model.predict_classes(x)
print('nice:', y)

x = get_padded_vector('fine effort')
y = model.predict_classes(x)
print('fine:', y)
