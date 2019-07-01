import pygame
import numpy as np
import math
import os

pygame.init()

WHITE = (255, 255, 255)
GREY = (20, 20, 20)
BLACK = (0, 0, 0)
PURPLE = (100, 0, 100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE_INT = 16777215
BLACK_INT = 0

WORLD_SIZE = (700, 500)
ROBOT_SIZE = 50
VERTICAL_LINE = 501
INFO_TEXT = VERTICAL_LINE + 9

screen = pygame.display.set_mode(WORLD_SIZE)
screen.fill(WHITE)

pygame.display.set_caption("Simple Map")

FILE = 'prob.npy'


class World:

    def __init__(self):

        self.draw_line(VERTICAL_LINE, 0, 1, 500, BLACK)
        self.background = np.copy(self.get_surface())
        self.state = self.background
        self.targets = []
        self.load_targets()
        self.target = None
        self.selected_target = None
        self.colors = [WHITE, BLACK, RED, BLUE, PURPLE, GREY]
        pygame.font.init()
        self.font = pygame.font.SysFont('David', 20)
        self.reset()
        self.turn = 0
        self.position = 0
        self.actions = []

    def reset(self):
        pygame.surfarray.blit_array(pygame.display.get_surface(), self.background)

        self.selected_target = np.random.randint(0, len(self.targets))
        self.target = self.targets[self.selected_target]
        self.turn = 0
        self.position = 0
        self.actions = []

    def load_targets(self):

        if os.path.exists(FILE):
            self.targets = np.load(FILE)
            return

        nn = np.random.choice(10, 10, p=[.1, .15, .05, .1, .2, .1, .2, .01, .07, .02])

        for n in nn:
            targets = [[n, 1]]

            next = n
            for i in range(9):
                next = math.floor(np.random.normal(next, 1))
                if next < 0:
                    next = 0
                elif next > 9:
                    next = 9

                targets.append([next + 10 + i * 10, 1])

            self.targets.append(targets)

        self.targets = np.asanyarray(self.targets, dtype=int)
        np.save(FILE, self.targets)

    @staticmethod
    def get_surface():
        return pygame.surfarray.pixels2d(screen)

    def get_location_vector(self, location):

        x = location[0] % 10 * ROBOT_SIZE
        y = location[0] // 10 * ROBOT_SIZE

        return [x, y, location[1]]

    def draw(self, prob=None):

        pygame.surfarray.blit_array(pygame.display.get_surface(), self.background)

        if prob is not None:
            self.draw_prob(prob, 10)

        for target in self.target:
            position = self.get_location_vector(target)

            pygame.draw.rect(screen, self.colors[position[2]], (position[0], position[1], ROBOT_SIZE, ROBOT_SIZE))

        line = 150
        self.draw_text('Selected: {}'.format(self.selected_target), (INFO_TEXT, line), RED)
        line += 20
        self.draw_text('Turn: {}'.format(self.turn), (INFO_TEXT, line), RED)
        line += 20
        self.draw_text('Position: {}'.format(self.position), (INFO_TEXT, line), RED)

        for a in self.actions:
            line += 20
            self.draw_text('action: {}'.format(a), (INFO_TEXT, line), BLUE)

        pygame.display.flip()

    def draw_rec(self, x, y, size, color):
        pygame.draw.rect(screen, color, pygame.Rect(x, y, size, size))

    def draw_line(self, x, y, x_, y_, color):
        pygame.draw.rect(screen, color, pygame.Rect(x, y, x_, y_))

    def draw_text(self, text, position, color):
        txt = self.font.render(text, True, color)
        screen.blit(txt, position)

    def draw_prob(self, prob, y):

        x = INFO_TEXT
        for i in range(len(prob)):
            p = prob[i] * 200
            self.draw_line(x, y, 10, p, GREEN)
            x += 15

    @staticmethod
    def update_display():
        pygame.display.update()

    def take_action(self, action):

        if self.turn == 10:
            return 0, 0, True

        self.actions.append(action)

        obs, reward, done = 0, 0, False
        if self.target[self.position][0] == action + 10 * self.position:
            self.position += 1
            obs, reward = 1, 1

        self.turn += 1
        # obs, reward, done
        return obs, reward, done
