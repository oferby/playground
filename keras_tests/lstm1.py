import os

from keras.layers import LSTM, Input, Dense
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
    encoder_inputs = Input((1,1))
    encoder_lstm = LSTM(n_neurons, return_state=True, name="encoder_lstm")

    encoder_outputs, encoder_state_h, encoder_state_c = encoder_lstm(encoder_inputs)
    encoder_states = [encoder_state_h, encoder_state_c]

    model.add(encoder_lstm)
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(X, y, epochs=n_epoch, batch_size=n_batch, verbose=2)
    model.save(FILE_NAME)

print(model.summary())

# evaluate
result = model.predict(X, batch_size=n_batch, verbose=0)
for i, value in enumerate(result):
    print('%.1f' % X[i][0], value)
