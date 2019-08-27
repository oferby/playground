import os
import random

import numpy as np
import pygame

pygame.init()

WHITE = (255, 255, 255)
GREY = (20, 20, 20)
BLACK = (0, 0, 0)
PURPLE = (100, 0, 100)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

COLOR0 = (70, 70, 70)
COLOR1 = (50, 100, 200)
COLOR2 = (100, 200, 100)
COLOR3 = (150, 100, 100)
COLOR4 = (90, 40, 40)
COLOR5 = (55, 100, 70)
COLOR6 = (25, 80, 55)
COLOR7 = (155, 40, 90)
COLOR8 = (75, 20, 80)
COLOR9 = (65, 90, 10)

WHITE_INT = 16777215
BLACK_INT = 0

WORLD_SIZE = (1000, 1000)
ROBOT_SIZE = 50

DIM = int(1000 / 50)
OPERATIONS = 4  # left, up, right, down
OBSERVATIONS = 10  # 0-9

screen = pygame.display.set_mode(WORLD_SIZE)

pygame.display.set_caption("Simple Maze")

MAP_FILE = 'data\map.npy'
STATES_FILE = 'data\stats.npy'


class World:

    def __init__(self):

        self.agent_location = np.zeros((DIM, DIM))
        self.obstacles = np.zeros((DIM, DIM))

        self.T = np.zeros((DIM * DIM, DIM * DIM))
        self.Z = np.zeros((OBSERVATIONS, DIM * DIM))
        self.A = np.zeros((4, DIM * DIM))

        self.prior = np.ones(DIM * DIM) * (1 / (DIM * DIM))
        self.show_prior = True

        self.init_target_location()
        self.background = np.copy(self.get_surface())
        self.agent_location = self.init_agent_location()
        self.show_agent = False
        self.add_noise = False

        pygame.font.init()
        self.font = pygame.font.SysFont('David', 20)

    def toggle_show_agent(self):
        self.show_agent = not self.show_agent

    def toggle_show_prior(self):
        self.show_prior = not self.show_prior

    def init_agent_location(self):
        x = random.randint(0, DIM - 1)
        y = random.randint(0, DIM - 1)
        return [x, y]

    def init_target_location(self):

        if os.path.exists(MAP_FILE):
            self.obstacles = np.load(MAP_FILE)
        else:
            for i in range(DIM):
                for j in range(DIM):
                    self.obstacles[i][j] = random.randint(0, OBSERVATIONS - 1)
            np.save(MAP_FILE, self.obstacles)

        if os.path.exists(STATES_FILE):
            stats = np.load(STATES_FILE)
        else:
            self.calc_states()

        screen.fill(WHITE)

        for i in range(DIM):
            for j in range(DIM):
                position = self.get_location_vector([i, j])
                color_num = self.obstacles[i][j]
                if color_num == 0:
                    color = COLOR0
                elif color_num == 1:
                    color = COLOR1
                elif color_num == 2:
                    color = COLOR2
                elif color_num == 3:
                    color = COLOR3
                elif color_num == 4:
                    color = COLOR4
                elif color_num == 5:
                    color = COLOR5
                elif color_num == 6:
                    color = COLOR6
                elif color_num == 7:
                    color = COLOR7
                elif color_num == 8:
                    color = COLOR8
                else:
                    color = COLOR9

                pygame.draw.rect(screen, color, (position[0], position[1], ROBOT_SIZE, ROBOT_SIZE))

    def calc_states(self):
        for i in range(DIM * DIM):
            for j in range(DIM * DIM):
                if i == j or i - DIM == j or i + DIM == j or i == j - 1 or i == j + 1:
                    self.T[i, j] += 1

        for i in range(DIM * DIM):
            s = sum(self.T[i, 0:DIM * DIM])
            for j in range(DIM * DIM):
                if self.T[i, j] > 0:
                    self.T[i, j] = self.T[i, j] / s

        #     calc Z
        for i in range(DIM):
            for j in range(DIM):
                obs = int(self.obstacles[i, j])
                self.Z[obs, i * DIM + j] += 1

        # print('real: {}'.format(self.obstacles[0]))
        # print('Z: {}'.format(self.Z[:, 0:DIM]))

        #     normalize Z
        for i in range(OBSERVATIONS):
            s = sum(self.Z[i])
            for j in range(DIM * DIM):
                self.Z[i][j] = self.Z[i][j] / s

        # print('Znorm: {}'.format(self.Z[0, 0:DIM]))

    @staticmethod
    def get_surface():
        return pygame.surfarray.pixels2d(screen)

    def draw(self, prior):

        pygame.surfarray.blit_array(pygame.display.get_surface(), self.background)

        if self.show_agent:
            position = self.get_location_vector(self.agent_location)
            pygame.draw.rect(screen, RED, (position[0], position[1], 10, 10))

        if self.show_prior:
            for i in range(DIM):
                for j in range(DIM):
                    p = prior[i * DIM + j]
                    if p < 0.1:
                        size = 5
                    elif p < 0.2:
                        size = 10
                    elif p < 0.3:
                        size = 15
                    else:
                        size = 20
                    position = self.get_location_vector([i, j])
                    pygame.draw.rect(screen, BLACK, (position[0] + ROBOT_SIZE - size, position[1], size, size))

        pygame.display.flip()

    def get_location_vector(self, location):
        x = location[1] * ROBOT_SIZE
        y = location[0] * ROBOT_SIZE
        return [x, y]

    def draw_rec(self, x, y, size, color):
        pygame.draw.rect(screen, color, pygame.Rect(x, y, size, size))

    def draw_text(self, text, position, color):
        txt = self.font.render(text, True, color)
        screen.blit(txt, position)

    @staticmethod
    def update_display():
        pygame.display.update()

    def take_action(self, action):

        new_position = self.agent_location.copy()

        if action == 0:
            new_position[0] -= 1
        elif action == 1:
            new_position[1] += 1
        elif action == 2:
            new_position[0] += 1
        elif action == 3:
            new_position[1] -= 1

        if self.is_move_valid(new_position):
            self.agent_location = new_position

        # obs, reward, done
        # obs = self.obstacles[self.agent_location[0], self.agent_location[1]]
        obs = self.get_obs_distribution()
        print(self.agent_location)
        return obs, 0, False

    def get_obs_distribution(self):
        obs = np.zeros(OBSERVATIONS)
        obs[int(self.obstacles[self.agent_location[0], self.agent_location[1]])] = 1

        if self.add_noise:
            if self.agent_location[0] > 0:
                obs[int(self.obstacles[self.agent_location[0] - 1, self.agent_location[1]])] = .9
                if self.agent_location[1] > 0:
                    obs[int(self.obstacles[self.agent_location[0] - 1, self.agent_location[1] - 1])] = .8
                if self.agent_location[1] < DIM - 1:
                    obs[int(self.obstacles[self.agent_location[0] - 1, self.agent_location[1] + 1])] = .8

            if self.agent_location[0] < DIM - 1:
                obs[int(self.obstacles[self.agent_location[0] + 1, self.agent_location[1]])] = .7
                if self.agent_location[1] > 0:
                    obs[int(self.obstacles[self.agent_location[0] + 1, self.agent_location[1] - 1])] = .8
                if self.agent_location[1] < DIM - 1:
                    obs[int(self.obstacles[self.agent_location[0] + 1, self.agent_location[1] + 1])] = .8

            if self.agent_location[1] > 0:
                obs[int(self.obstacles[self.agent_location[0], self.agent_location[1] - 1])] = .9

            if self.agent_location[1] < DIM - 1:
                obs[int(self.obstacles[self.agent_location[0], self.agent_location[1] + 1])] = .6

            # normalize
            s = sum(obs)
            for i in range(OBSERVATIONS):
                obs[i] /= s

        return obs

    def is_move_valid(self, position):

        if position[0] > DIM - 1 or position[0] < 0 or position[1] > DIM - 1 or position[1] < 0:
            return False

        return True
