import abc
import random
import numpy as np


class AbstractAgent:

    def __init__(self, state_space, action_space, name=None):
        self.state_space = state_space
        self.action_space = action_space
        self.name = name

    @abc.abstractmethod
    def get_action(self, state):
        pass

    @abc.abstractmethod
    def observe(self, observation, reward, done):
        pass


class RandomAgent(AbstractAgent):

    def get_action(self, state):
        return np.random.randint(0, self.action_space)

    def observe(self, observation, reward, done):
        if done:
            print('{} my reward: {}'.format(self.name, reward))
