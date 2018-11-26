import sys
from abc import abstractmethod
from collections import deque

import numpy as np
import pygame
from keras.layers import Dense, LSTM, TimeDistributed
from keras.models import Sequential


class Agent:
    @abstractmethod
    def get_action(self, obs):
        pass


class RandomAgent(Agent):
    def __init__(self):
        self.actions = [0, 1, 2, 3]

    def get_action(self, obs):
        r = np.random.random_integers(0, 3)
        return r


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
        self.model.add(LSTM(100))
        self.model.add(Dense(4))
        self.model.compile('RMSProp', 'mse')

        self.memory = deque(maxlen=20000)

    def get_action(self, obs):
        a, _ = self.predit(obs)
        return a

    def remember(self, obs, action, reward, done):
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
