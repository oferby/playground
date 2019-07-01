import sys
from abc import abstractmethod
import numpy as np
import pandas as pd

import pygame

SENSOR_NOISE = 20.0


def kb_action():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYUP:
            k = event.key
            # print('key:', k)
            # q
            if k == 113:
                sys.exit()

            if k == 48:
                return 0
            elif k == 49:
                return 1
            elif k == 50:
                return 2
            elif k == 51:
                return 3
            elif k == 52:
                return 4
            elif k == 53:
                return 5
            elif k == 54:
                return 6
            elif k == 55:
                return 7
            elif k == 56:
                return 8
            elif k == 57:
                return 9
            # r
            elif k == 114:
                return 99
            # s
            elif k == 115:
                return 98
            # p
            elif k == 112:
                return 97
    return


class Agent:
    @abstractmethod
    def get_action(self, obs):
        pass

    def get_observation(self, obs, action, reward, done):
        print("action: ", action, "obs: ", obs, "reward: ", reward, 'done:', done)


class SimpleAgent(Agent):

    def get_action(self, obs):
        return kb_action()


class StatisticalAgent(Agent):

    def __init__(self, map):
        self.state = self.calc_probabilities(map)
        self.policy = None
        self.obs = None

    def calc_probabilities(self, map):
        return np.ones(10) * .2

    def get_action(self, obs):
        return kb_action()

    def get_state_prob(self):
        return self.state
