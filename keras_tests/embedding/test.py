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
        'Could have done better.']

for d in docs:
    print(d, T.one_hot(d, 10))
