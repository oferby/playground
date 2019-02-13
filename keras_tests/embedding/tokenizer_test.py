import keras.preprocessing.text as T

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
    'not nice',
    'neat'
]

# prepare tokenizer
t = T.Tokenizer()


t.fit_on_texts(docs)

vocab_size = len(t.word_index) + 1

print (t.word_docs.items())
print(t.word_index)

t.fit_on_texts(more_docs)

vocab_size = len(t.word_index) + 1

print (t.word_docs.items())
print(t.word_index)

print('nice:',t.word_index['nice'])


json_string  = t.to_json()

t = None
t = T.text.tokenizer_from_json(json_string)

print('nice after loading:',t.word_index['nice'])
