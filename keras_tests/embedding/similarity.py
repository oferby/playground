import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

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

x = np.expand_dims(embeddings_index.get('good'), 0)
y = np.expand_dims(embeddings_index.get('bad'), 0)

print('cosine similarity for good vs. bad: ', cosine_similarity(x, y))

x = np.expand_dims(embeddings_index.get('good'), 0)
y = np.expand_dims(embeddings_index.get('good'), 0)

print('cosine similarity for good vs. good: ', cosine_similarity(x, y))

x = np.expand_dims(embeddings_index.get('king'), 0)
y = np.expand_dims(embeddings_index.get('queen'), 0)

print('cosine similarity for king vs. queen: ', cosine_similarity(x, y))

