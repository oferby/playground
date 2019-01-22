import sys
from abc import abstractmethod
from collections import deque

import numpy as np
import pygame
from keras.layers import Dense, TimeDistributed
from keras.models import Sequential


class Agent:
    @abstractmethod
    def get_action(self, obs):
        pass

    def get_feedback(self, obs, action, reward, done):
        pass


class RandomAgent(Agent):

    def get_action(self, obs):
        r = np.random.random_integers(0, 3)
        return r


class LineAgent(Agent):
    def __init__(self):
        self.last_action = self.get_random_action()
        self.last_obs = [0, 0, 0, 0]

    def get_action(self, obs):
        if np.array_equal(obs, self.last_obs):
            self.last_action = self.get_random_action()
            return self.last_action
        else:
            self.last_obs = obs
            return self.last_action

    def get_random_action(self):
        return np.random.random_integers(0, 3)


class SimpleAgent(Agent):

    def get_action(self, obs):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYUP:
                k = event.key
                if k == 273:
                    return 0
                elif k == 274:
                    return 2
                elif k == 275:
                    return 1
                elif k == 276:
                    return 3
        return


class QmdpAgent(Agent):
    def __init__(self):
        pass


class QpomdpAgent(Agent):

    def __init__(self):
        self.model = Sequential()
        self.model.add(TimeDistributed(Dense(32), input_shape=(4, 1)))
        self.model.add(TimeDistributed(Dense(8)))
        # self.model.add(LSTM(100))
        self.model.add(Dense(4))
        self.model.compile('RMSProp', 'mse')
        self.memory = deque(maxlen=20000)
        self.count_to_training = 0
        self.epsilon = 1.
        self.decay = 0.9999
        self.threshold = 0.1

    def get_action(self, obs):

        self.count_to_training += 1
        if self.count_to_training == 200:
            self.train()
            self.count_to_training = 0

        r = np.random.random()
        if 1 - self.epsilon < r:
            if self.epsilon > self.threshold:
                self.epsilon *= self.decay
            return self.get_random_action()

        a, _ = self.predit(obs)
        return a

    def get_random_action(self):
        return np.random.random_integers(0, 3)

    def get_feedback(self, obs, action, reward, done):
        self.memory.append((obs, action, reward, done))

    def predit(self, obs):
        obs = np.reshape(obs, [1, 4, 1])
        actions = self.model.predict(obs)
        return np.argmax(actions), actions

    def train(self):
        choices = np.random.choice(self.memory, 8)
        observations = []
        actions = []
        for choice in choices:
            obs, action, reward, done = self.memory[choice]
            if done:
                continue
            i = 0
            while not done:
                i += 1
                obs, action, reward, done = self.memory[choice + i]
