import os

import keras.preprocessing.sequence as S
import keras.preprocessing.text as T
import numpy as np
from keras.layers import Embedding, Dense, Flatten
from keras.models import Sequential
from keras.models import model_from_json

NUMPY_FILE_NAME_PADDED = 'padded_docs_glove.npy'
NUMPY_FILE_NAME_OTHER = 'padded_other_glove.npy'

# define documents
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
max_length = 4

# prepare tokenizer
t = T.Tokenizer()

all_docs = np.append(docs, more_docs)

t.fit_on_texts(all_docs)
vocab_size = len(t.word_index) + 1


def create_or_load_docs():
    if os.path.isfile(NUMPY_FILE_NAME_PADDED):
        padded_docs = np.load(NUMPY_FILE_NAME_PADDED)
        padded_other = np.load(NUMPY_FILE_NAME_OTHER)
    else:
        # integer encode the documents
        encoded_docs = t.texts_to_sequences(docs)
        # print(encoded_docs)

        encoded_others = t.texts_to_sequences(more_docs)
        padded_other = S.pad_sequences(encoded_others, maxlen=max_length, padding='post')
        print('other docs:\n', padded_other)

        # pad documents to a max length of 4 words
        padded_docs = S.pad_sequences(encoded_docs, maxlen=max_length, padding='post')

        np.save(NUMPY_FILE_NAME_PADDED, padded_docs)
        np.save(NUMPY_FILE_NAME_OTHER, padded_other)

        print(padded_docs)

    return padded_docs, padded_other


def create_model():
    # load the whole embedding into memory
    print('loading Glove...')
    embeddings_index = dict()
    f = open('../../data/glove.6B.100d.txt', encoding='utf-8-sig')
    for line in f:
        values = line.split()
        word = values[0]
        coefs = np.asarray(values[1:], dtype='float32')
        embeddings_index[word] = coefs
    f.close()
    print('Loaded %s word vectors.' % len(embeddings_index))

    # create a weight matrix for words in training docs
    embedding_matrix = np.zeros((vocab_size, 100))
    for word, i in t.word_index.items():
        print('adding word:', word)
        embedding_vector = embeddings_index.get(word)
        if embedding_vector is not None:
            embedding_matrix[i] = embedding_vector

    print(embedding_matrix)

    model = Sequential()
    model.add(Embedding(vocab_size, 100, weights=[embedding_matrix], input_length=max_length, trainable=False))
    model.add(Flatten())
    model.add(Dense(1, activation='sigmoid'))
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['acc'])
    print(model.summary())

    # fit the model
    model.fit(padded_docs, labels, epochs=200, verbose=1)

    # serialize model to JSON
    model_json = model.to_json()
    with open("model-glove.json", "w") as json_file:
        json_file.write(model_json)
    # serialize weights to HDF5
    model.save_weights("model-glove.h5")
    print("Saved model to disk")
    return model


def load_model():
    # load json and create model
    json_file = open('model-glove.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights("model-glove.h5")
    loaded_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['acc'])
    print("Loaded model from disk")
    return loaded_model


def create_or_load_model():
    if os.path.isfile("model-glove.json"):
        return load_model()
    return create_model()


padded_docs, padded_other = create_or_load_docs()
model = create_or_load_model()
# evaluate
loss, accuracy = model.evaluate(padded_docs, labels, verbose=0)
print('Accuracy:', accuracy, 'Loss:', loss)

p = np.expand_dims(padded_docs[2], 0)
y = model.predict(p, 1)
print('y:', y)

# p = np.expand_dims(padded_other[1], 0)
y = model.predict(padded_other, 1)
print('y other:\n', y)
