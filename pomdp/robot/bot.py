import os
import numpy as np

from keras.models import Sequential, load_model
from keras.layers import Dense
from keras.optimizers import SGD, RMSprop

from collections import deque

MODEL_FILENAME = 'model1.h5'

states_dict = {

    'targetStraightBelow': 1,
    'targetBelowRight': 2,
    'targetBelowLeft': 3,

    'targetStraightAbove': 4,
    'targetAboveRight': 5,
    'targetAboveLeft': 6,

    'targetStraightRight': 7,
    'targetRightAbove': 8,
    'targetRightBelow': 9,

    'targetStraightLeft': 10,
    'targetLeftAbove': 11,
    'targetLeftBelow': 12,

    'openingStraightBelow': 13,
    'openingBelowRight': 14,
    'openingBelowLeft': 15,

    'openingStraightAbove': 16,
    'openingAboveRight': 17,
    'openingAboveLeft': 18,

    'openingStraightRight': 19,
    'openingRightAbove': 20,
    'openingRightBelow': 21,

    'openingStraightLeft': 22,
    'openingLeftAbove': 23,
    'openingLeftBelow': 24,
}


def create_model(actions, observations):
    model = Sequential()
    model.add(Dense(24, input_shape=(observations,), activation='relu'))
    model.add(Dense(48, activation='relu'))
    model.add(Dense(actions))
    # , activation='linear'
    model.compile(loss='mse', optimizer=SGD(lr=0.01))
    return model


class Robot:
    def __init__(self):
        self.memory = deque(maxlen=1000)
        self.sensor_range = 400
        self.memory_entry = 0
        self.sensors = [self.sensor_range, self.sensor_range, self.sensor_range, self.sensor_range,
                        0]  # left, up, right, down, goal detected

        if os.path.isfile(MODEL_FILENAME):
            print('loading model from file')
            self.model = load_model(MODEL_FILENAME)
        else:
            print('creating new model')
            self.model = create_model(4, 5)
            self.model.save(MODEL_FILENAME)

    def remember(self, o, a, r, done):
        self.memory.append([o, a, r, done])
        if done or self.memory_entry > 100:
            self.memory_entry = 0
            self.train()

    def train(self):
        samples = np.random.choice(self.memory_entry, 32)
        obs = []
        actions = []
        for sample in samples:
            o, a, r, done = sample
            obs.append(o)
            actions.append(a)

    # robot can move [left, up, right, down]
    def take_action(self):
        actions = self.get_actions_values()
        action = np.argmax(actions)
        return action, actions

    def act_greedy(self, actions):
        pass

    def act_prob(self, actions):
        pass

    def get_actions_values(self):
        return self.model.predict([[self.sensors]])

    def get_sensors(self):
        return self.sensors

    def update_sensors(self, observation):
        self.sensors[4] = 0
        world = observation[0]
        y = observation[1][0]
        x = observation[1][1]
        if x < self.sensor_range:
            line = world[y][0:x]
        else:
            line = world[y][x - self.sensor_range:x]
        self.update_sensor(line[::-1], 0)
        if y < self.sensor_range:
            line = world[0:y][:, x]
        else:
            line = world[y - self.sensor_range: y][:, x]
        self.update_sensor(line[::-1], 1)

        if x + self.sensor_range > world.shape[1]:
            line = world[y][x:world.shape[0]]
        else:
            line = world[y][x: x + self.sensor_range]
        self.update_sensor(line, 2)

        if y + self.sensor_range > world.shape[0]:
            line = world[y:world.shape[1]][:, x]
        else:
            line = world[y: y + self.sensor_range][:, x]
        self.update_sensor(line, 3)

    def update_sensor(self, line, sensor_num):
        found = False
        for i, pos in enumerate(line):
            if not np.array_equal(pos, [0, 0, 0]):
                self.sensors[sensor_num] = i - 10
                found = True
                if np.array_equal(pos, [0, 0, 255]):
                    self.sensors[4] = 1
                break
        if not found:
            self.sensors[sensor_num] = self.sensor_range
