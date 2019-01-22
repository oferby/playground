import os

from keras.layers import Dense
from keras.layers import LSTM
from keras.models import Sequential, load_model
from numpy import array

FILE_NAME = "model.h5"
# prepare sequence
length = 10
seq = array([i / float(length) for i in range(length)])
X = seq[:-1]
X = X.reshape(len(X), 1, 1)
y = seq[1:]
y = y.reshape(len(y), 1)
# define LSTM configuration
n_neurons = length
n_batch = length
n_epoch = 1000

# load or create LSTM

if os.path.isfile(FILE_NAME):
    model = load_model(FILE_NAME)
else:
    model = Sequential()
    model.add(LSTM(n_neurons, input_shape=(1, 1)))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(X, y, epochs=n_epoch, batch_size=n_batch, verbose=2)

print(model.summary())
# train LSTM

model.save(FILE_NAME)
# evaluate
result = model.predict(X, batch_size=n_batch, verbose=0)
for i, value in enumerate(result):
    print('%.1f' % value, X[i][0])
