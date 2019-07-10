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

    def __init__(self, targets):
        self.action_size = targets.shape[0] * targets.shape[1]
        self.turn_size = targets.shape[1]
        self.policy = None
        self.obs = None
        self.reset(targets)

    def reset(self, targets):
        self.turn = 0
        self.prior = None
        self.state = None
        self.action_prob = None
        self.joint_probability = None
        self.action_given_turn = None
        self.action_joint_turn = None
        self.calc_probabilities(targets)

    def calc_probabilities(self, targets):
        size = targets.shape[0]

        # state priors
        goals = np.zeros(size)

        action_prob = np.zeros(self.action_size)
        joint_prob = np.zeros((size, self.action_size))

        action_given_turn = np.zeros((self.turn_size, self.action_size))

        for target in targets:

            g = target[-1][0] - 90
            goals[g] += 1

            for i, action in enumerate(target):
                a = action[0]
                action_prob[a] += 1
                joint_prob[g][a] += 1
                action_given_turn[i][a] += 1

        for i in range(action_given_turn.shape[0]):
            s = sum(action_given_turn[i])
            for j in range(action_given_turn.shape[1]):
                action_given_turn[i][j] = action_given_turn[i][j] / s

        prior = [x / size for x in goals]
        print('Goal Prior: {}'.format(prior))

        action_prob = [x / size for x in action_prob]
        print('Action Probability: {}'.format(action_prob))

        self.prior = prior
        self.state = prior
        self.action_prob = action_prob
        self.joint_probability = joint_prob
        self.action_given_turn = action_given_turn

        # checking joint prob between turn and action
        self.action_joint_turn = self.calc_joint_prob()

    def get_action(self, obs):

        action = kb_action()
        return action

    def calc_joint_prob(self):
        turn = np.zeros(self.turn_size)
        turn[self.turn] = 1
        turn = np.matrix(turn)
        action_joint_turn = np.matrix(turn) * self.action_given_turn
        # print(action_joint_turn)
        return action_joint_turn

    def get_state_prob(self):
        pr = np.squeeze(np.asarray(self.action_joint_turn))
        return (self.state, pr)

    def get_observation(self, obs, action, reward, done):

        if reward == 1:
            self.turn += 1
            self.action_joint_turn = self.calc_joint_prob()

        super().get_observation(obs, action, reward, done)

        if done:
            self.reset()
            return
