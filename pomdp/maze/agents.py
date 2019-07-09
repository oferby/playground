import sys
from abc import abstractmethod
from math import *

import numpy as np
import pygame

import sys
sys.path.insert(0, "./")

import world as W

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

            if k == 273:
                return 0
            elif k == 274:
                return 2
            elif k == 275:
                return 1
            elif k == 276:
                return 3
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

    def get_feedback(self, obs, action, reward, done):
        print("action: ", action, "obs: ", obs, "reward: ", reward)


class SimpleAgent(Agent):

    def __init__(self):
        self.state = [0,0,0,0]

    def get_action(self, obs):
        return kb_action()

