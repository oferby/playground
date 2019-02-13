import os

import keras.preprocessing.sequence as S
import keras.preprocessing.text as T
import keras.utils as U
import numpy as np
from keras.layers import Embedding, Dense, LSTM
from keras.models import Sequential
from keras.models import model_from_json
import json

questions = []
answers = []

max_length = 20

MODEL_FILE = "predict-model.json"
WEIGHTS_FILE = "predict-weights.h5"
TOKENIZER_FILE = 'predict-tokenizer.json'


def tokenize_text():
    json_file = open('./data/q_and_a.json', 'r')
    data = json_file.read()
    data = json.loads(data)

    for qas in data['data']:
        for q in qas['qas']:
            for a in q['answers']:
                q_text = q['question']
                questions.append(q_text)
                answers.append(a['text'])

    t = T.Tokenizer()
    t.fit_on_texts(questions)
    t.fit_on_texts(answers)

    json_file = open(TOKENIZER_FILE, 'w')
    json_file.write(t.to_json())

    return t


def get_vector(text):
    vec = t.texts_to_sequences(text)
    padded_vec = S.pad_sequences(vec, maxlen=max_length, padding='post')
    return padded_vec


def load_embeddings():
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
    return embeddings_index


def get_wordvec():
    embeddings_index = load_embeddings()
    embedding_matrix = np.zeros((vocab_size, 100))
    for word, i in t.word_index.items():
        embedding_vector = embeddings_index.get(word)
        if embedding_vector is not None:
            embedding_matrix[i] = embedding_vector
    return embedding_matrix


def get_training_set():
    X = get_vector(questions)
    Y = np.arange(len(questions))
    Y = U.to_categorical(Y, len(questions))
    return X, Y


def create_or_load_model():
    embedding_matrix = get_wordvec()

    model = Sequential()
    model.add(Embedding(vocab_size, 100, weights=[embedding_matrix], input_length=max_length, trainable=False))
    model.add(LSTM(1024))
    model.add(Dense(len(answers), activation='sigmoid'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['acc'])
    print(model.summary())

    # fit the model
    X, Y = get_training_set()
    model.fit(X, Y, epochs=500, verbose=1)

    model_json = model.to_json()
    with open(MODEL_FILE, "w") as json_file:
        json_file.write(model_json)
    model.save_weights(WEIGHTS_FILE)
    print("Saved model to disk")
    return model


t = tokenize_text()
vocab_size = len(t.word_index) + 1
print('vocab size:', vocab_size)

question = 'what other entertainment venture did Beyonce explore?'
q_vec = get_vector([question])
print('question vector":', q_vec)

model = create_or_load_model()
clzz = model.predict_classes(q_vec)[0]
print(clzz, ':', questions[clzz], answers[clzz])
