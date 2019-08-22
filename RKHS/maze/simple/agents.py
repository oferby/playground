import sys
from abc import abstractmethod

import numpy as np
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

            if k == 273:
                return 0  # up
            elif k == 274:
                return 2  # down
            elif k == 275:
                return 1  # right
            elif k == 276:
                return 3  # left
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


class BayesAgent(Agent):

    def __init__(self, world):
        self.Tm = np.matrix(world.T)
        self.Zm = np.matrix(world.Z)
        self.observations = len(world.Z)
        self.prior = world.prior
        self.prior_dim = int(np.sqrt(len(self.prior)))

        self.obstacles = world.obstacles

    def flatten(self, a):
        return np.asarray(a).reshape(-1)

    def get_action(self, obs):
        action = kb_action()
        return action

    def normalize(self, arr):
        s = arr.sum()
        if s == 0:
            return arr
        return arr / s

    def update_move(self, action):
        dim = self.prior_dim
        prior = self.prior.reshape(dim, dim)
        zz = np.matrix(np.zeros(dim))
        if action == 0:
            p_ = prior[1:, :]
            prior = np.vstack([p_, zz])
        elif action == 1:
            p_ = prior[:, 0:-1]
            prior = np.hstack([zz.transpose(), p_])
        elif action == 2:
            p_ = prior[0:-1, :]
            prior = np.vstack([zz, p_])
        else:
            p_ = prior[:, 1:]
            prior = np.hstack([p_, zz.transpose()])

        prior = self.normalize(prior)
        self.prior = self.flatten(prior)

    def update_observation(self):
        pass

    def get_observation(self, obs, action, reward, done):
        super().get_observation(obs, action, reward, done)

        self.update_move(action)

        pZ = self.get_obs_vector(int(obs))
        posterior = self.flatten(pZ * self.Zm)  # * self.flatten(self.prior)
        # self.prior = posterior
        # print('real: {}'.format(self.obstacles[0]))
        print('state: {}'.format(self.prior[0:10]))

    def get_obs_vector(self, obs):
        z = np.zeros(self.observations)
        z[obs] = 1
        return np.matrix(z)
