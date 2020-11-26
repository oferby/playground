import tensorflow as tf
import tensorflow.keras
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras import layers
import xml.etree.ElementTree as ET
import nltk
import numpy as np

tree = ET.parse("../../data/blog.xml")

# get root element
root = tree.getroot()

# iterate post items
posts = []
for post in root.findall('post'):
    posts.append(post.text.lower().replace('\n', ' '))

sentences = []
for p in posts:
    tkn = nltk.sent_tokenize(p)
    for t in tkn:
        s = t.strip()
        sentences.append(s)
        # print(s)

# word embedding
vocab_size = 10000
embedding_dim = 16
max_length = 100
trunc_type = 'post'
padding_type = 'post'
oov_tok = "<OOV>"
training_size = 180

training_sentences = sentences[0:training_size]
testing_sentences = sentences[training_size:]

tokenizer = Tokenizer(num_words=vocab_size, oov_token=oov_tok)
tokenizer.fit_on_texts(training_sentences)

word_index = tokenizer.word_index

training_sequences = tokenizer.texts_to_sequences(training_sentences)
training_padded = pad_sequences(training_sequences, maxlen=max_length, padding=padding_type, truncating=trunc_type)

testing_sequences = tokenizer.texts_to_sequences(testing_sentences)
testing_padded = pad_sequences(testing_sequences, maxlen=max_length, padding=padding_type, truncating=trunc_type)

# Need this block to get it to work with TensorFlow 2.x
training_padded = np.array(training_padded)
testing_padded = np.array(testing_padded)

model = tf.keras.Sequential()
model.add(layers.Embedding(vocab_size, embedding_dim, input_length=max_length))

p = model.predict(training_padded[0])
print(p)
