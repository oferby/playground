from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

sentences = [
    "I love my dog.",
    "I love my cat",
    "You love my dog",
    "Do you think my dog is amazing?"
]

tokenizer = Tokenizer(num_words=100, oov_token="<OOV>")
tokenizer.fit_on_texts(sentences)
word_index = tokenizer.word_index
print(word_index)

sequences = tokenizer.texts_to_sequences(sentences)
print(sequences)

test_sentences = [
    "my dog love me"
]

test_sequences = tokenizer.texts_to_sequences(test_sentences)
print("\nout of vocabulary:")
print(test_sequences)

padded_sequences = pad_sequences(sequences)
print("\npadded:")
print(padded_sequences)
