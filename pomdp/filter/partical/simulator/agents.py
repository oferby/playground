import sys
from abc import abstractmethod
from math import *

import numpy as np
import pygame

import pomdp.filter.partical.simulator.world as W

SENSOR_NOISE = 10.0


class Agent:
    @abstractmethod
    def get_action(self, obs):
        pass

    def get_feedback(self, obs, action, reward, done):
        print("action: ", action, "obs: ", obs, "reward: ", reward)


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


class RobotParticle:
    def __init__(self, x, y, sensors, prob):
        self.prob = prob
        self.x = x
        self.y = y
        self.sensors = sensors


class ParticleFilteringAgent(Agent):

    def __init__(self, world):
        self.world = world
        self.particles = []
        self.init_particles(world)
        print('done creating particles')

    def init_particles(self, word):
        width, height = W.WORLD_SIZE
        size = W.ROBOT_SIZE
        num_of_particles = 100
        for i in range(num_of_particles):
            while True:
                x = np.random.randint(0, width)
                y = np.random.randint(0, height)
                if x + size > width or y + size > height:
                    continue
                isNotValidPlace = word.check_surface_for_position(x, y, size)
                if not isNotValidPlace:
                    break
            sensors = word.get_partial_obs(x, y)
            self.particles.append(RobotParticle(x, y, sensors, 1 / num_of_particles))

    def get_particles(self):
        p = []
        for i in range(len(self.particles)):
            p_ = self.particles[i]
            p.append([p_.x, p_.y, p_.prob])
        return p

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

    def get_feedback(self, obs, action, reward, done):
        self.update_belief(obs, action)

    def update_belief(self, obs, action):

        # update move
        s = set(self.particles)
        for i in range(len(self.particles)):
            p = self.particles[i]
            # up
            if action == 0:
                step = int(np.random.normal(W.STEP_SIZE, 1))
                new_location = (p.y - step) % W.height
                p.y = new_location

            # right
            elif action == 1:
                step = int(np.random.normal(W.STEP_SIZE, 1))
                new_location = (p.x + step) % W.width
                p.x = new_location

            # down
            elif action == 2:
                step = int(np.random.normal(W.STEP_SIZE, 1))
                new_location = (self.particles[i].y + step) % W.height
                self.particles[i].y = new_location

            # left
            elif action == 3:
                step = int(np.random.normal(W.STEP_SIZE, 1))
                new_location = (p.x - step) % W.width
                p.x = new_location

        # update measurement likelihood
        all_prob = []
        for i in range(len(self.particles)):
            prob = 1.0
            p = self.particles[i]
            sensors = self.particles[i].sensors = self.world.get_partial_obs(p.x, p.y)
            for j in range(len(obs)):
                prob *= self.Gaussian(sensors[j], SENSOR_NOISE, obs[j])
            p.prob = prob
            all_prob.append(prob)

        # normalize Z likelihood
        max_prob_index = np.argmax(all_prob)
        max_prob = all_prob[max_prob_index]
        # print(obs, self.particles[max_prob_index].sensors, max_prob)

        for i in range(len(self.particles)):
            self.particles[i].prob = all_prob[i] / max_prob

        new_particles = []
        N = len(self.particles)
        index = np.random.randint(0, N)
        beta = 0
        for i in range(N):
            beta += np.random.uniform(0, max_prob * 2)
            while all_prob[index] < beta:
                beta -= all_prob[index]
                index = (index + 1) % N
            p_x = self.particles[index].x
            p_y = self.particles[index].y
            p_prob = self.particles[index].prob
            p_sensors = self.particles[index].sensors
            new_particles.append(RobotParticle(p_x, p_y, p_sensors, p_prob))

        self.particles = new_particles
        # print('done measurement update. particles left: ', len(self.particles))

    def Gaussian(self, mu, sigma, x):
        # calculates the probability of x for 1-dim Gaussian with mean mu and var. sigma
        return exp(- ((mu - x) ** 2) / (sigma ** 2) / 2.0) / sqrt(2.0 * pi * (sigma ** 2))


class SelfGoingAgent(ParticleFilteringAgent):

    def __init__(self, world):
        super().__init__(world)
        self.path = np.ones(40)
        self.step = 0

    def get_action(self, obs):
        if self.step == len(self.path) - 1:
            return None
        else:
            self.step += 1
        return self.path[self.step]
