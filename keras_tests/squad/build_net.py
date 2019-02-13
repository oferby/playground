import os

import keras.preprocessing.sequence as S
import keras.preprocessing.text as T
import keras.utils as U
import numpy as np
from keras.layers import Embedding, Dense, Flatten, LSTM
from keras.models import Sequential
from keras.models import model_from_json
import json
from collections import deque

max_length = 50

questions = []
answers = []


def read_questions():
    print('reading questions and answers...')
    with open('./data/train-v2.0.json') as f:
        data = json.load(f)

    for d in data['data']:
        for p in d['paragraphs']:
            for q in p['qas']:
                if len(q['answers']) > 0:
                    # print('q:', q['question'])
                    for a in q['answers']:
                        # print('a:', a['text'])
                        a_ = a['text'].lower()
                        answers.append(a_)
                        questions.append(q['question'].lower())


def get_padded_text(to_pad):
    encoded_qs = t.texts_to_sequences(to_pad)
    padded_qs = S.pad_sequences(encoded_qs, maxlen=max_length, padding='post')
    return padded_qs


def create_or_load_tokenizer():
    if os.path.isfile('tokenizer.json'):
        print('loading tokenizer from file')
        json_file = open('tokenizer.json', 'r')
        t = T.text.tokenizer_from_json(json_file.read())
        vocab_size = len(t.word_index) + 1
        return t, vocab_size

    print('creating new tokenizer')
    t = T.Tokenizer()
    all_docs = np.append(questions, answers)
    t.fit_on_texts(all_docs)
    vocab_size = len(t.word_index) + 1

    json_file = open('tokenizer.json', 'w')
    json_file.write(t.to_json())

    return t, vocab_size


def load_model():
    # load json and create model
    json_file = open('model-squad.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights("model-squad.h5")
    loaded_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['acc'])
    print("Loaded model from disk")
    return loaded_model


def make_random(padded_qs, y):

    for i in range(int(len(padded_qs) / 10)):
        a = np.random.randint(0, len(padded_qs))
        b = np.random.randint(0, len(padded_qs))

        tmp = padded_qs[a]
        padded_qs[a] = padded_qs[b]
        padded_qs[b] = tmp

        tmp = y[a]
        y[a] = y[b]
        y[b] = tmp

    return padded_qs, y


def create_or_load_model():
    if os.path.isfile('model-squad.json'):
        return load_model()

    print('loading Glove...')
    embeddings_index = dict()
    f = open('../data/glove.6B.100d.txt', encoding='utf-8-sig')
    for line in f:
        values = line.split()
        word = values[0]
        coefs = np.asarray(values[1:], dtype='float32')
        embeddings_index[word] = coefs
    f.close()
    print('Loaded %s word vectors.' % len(embeddings_index))

    embedding_matrix = np.zeros((vocab_size, 100))
    for word, i in t.word_index.items():
        # print('adding word:', word)
        embedding_vector = embeddings_index.get(word)
        if embedding_vector is not None:
            embedding_matrix[i] = embedding_vector

    model = Sequential()
    model.add(Embedding(vocab_size, 100, weights=[embedding_matrix], input_length=max_length, trainable=False))
    model.add(LSTM(1024))
    model.add(Dense(len(answers), activation='sigmoid'))
    model.compile(loss='mean_squared_error', optimizer='sgd', metrics=['acc'])

    print(model.summary())

    padded_qs = get_padded_text(questions)
    y = np.arange(len(padded_qs))
    y = U.to_categorical(y, len(padded_qs))

    q, a = make_random(padded_qs, y)
    model.fit(q, a, epochs=1)

    model_json = model.to_json()
    with open("model-squad.json", "w") as json_file:
        json_file.write(model_json)
    # serialize weights to HDF5
    model.save_weights("model-squad.h5")
    print("Saved model to disk")

    return model, padded_qs


read_questions()
t, vocab_size = create_or_load_tokenizer()

model = create_or_load_model()

indx = 2
q = get_padded_text([questions[indx]])

a = model.predict_classes(q)
print(a)
