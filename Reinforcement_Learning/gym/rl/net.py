from keras.models import Sequential
from keras.layers import Dense


def get_model(n_actions, n_obs):
    model = Sequential()
    model.add(Dense(24, input_shape=(n_obs,), activation='relu'))
    model.add(Dense(48, activation='relu'))
    # model.add(Dense(24, activation='relu'))
    model.add(Dense(n_actions, activation='relu'))
    model.compile(optimizer='sgd',loss='mse')
    return model
