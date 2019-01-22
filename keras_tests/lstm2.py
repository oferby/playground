import os
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import TimeDistributed
from keras.models import Sequential, load_model
from numpy import array

FILE_NAME = "model2.h5"
# prepare sequence
length = 10
seq = array([i / float(length) for i in range(length)])
X = seq[:-1]
X = X.reshape(1, len(X), 1)
y = seq[1:]
y = y.reshape(1, len(y), 1)
# define LSTM configuration
n_neurons = length
n_batch = length
n_epoch = 1000

# create LSTM
if os.path.isfile(FILE_NAME):
    model = load_model(FILE_NAME)
else:
    model = Sequential()
    model.add(LSTM(n_neurons, input_shape=(length - 1, 1), return_sequences=True))
    model.add(TimeDistributed(Dense(1)))
    model.compile(loss='mean_squared_error', optimizer='adam')
    # train LSTM
    model.fit(X, y, epochs=n_epoch, batch_size=n_batch, verbose=2)

print(model.summary())

# evaluate
result = model.predict(X, batch_size=n_batch, verbose=0)
for i, value in enumerate(result[0, :, 0]):
    print('%.1f' % value, X[0][i])
