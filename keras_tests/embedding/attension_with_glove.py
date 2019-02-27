import keras.preprocessing.text as T
import numpy as np

input = ['hello, how are you today?']


def create_model():
    t = T.Tokenizer()
    t.fit_on_texts(input)
    vocab_size = len(t.word_index) + 1

    # load the whole embedding into memory
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

    # create a weight matrix for words in training docs
    embedding_matrix = np.zeros((vocab_size, 100))
    for word, i in t.word_index.items():
        print('adding word:', word)
        embedding_vector = embeddings_index.get(word)
        if embedding_vector is not None:
            embedding_matrix[i] = embedding_vector

    return embedding_matrix


def softmax(x):
    """Compute softmax values for each sets of scores in x."""
    return np.exp(x) / np.sum(np.exp(x), axis=0)


# embd = create_model()
# print(embd)
# np.save('data/embeddings.npy', embd)
embd = np.load('data/embeddings.npy')

qk = np.divide(np.dot(embd, np.transpose(embd)), 10)

qk_ = []
for x in qk:
    qk_.append(softmax(x))

assert qk is not None

for q in qk_:
    print(q)
