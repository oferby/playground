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

COLOR0 = (0, 0, 0)
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

WORLD_SIZE = (500, 500)
ROBOT_SIZE = 50

screen = pygame.display.set_mode(WORLD_SIZE)

pygame.display.set_caption("Simple Maze")


class World:

    def __init__(self):
        screen.fill(WHITE)
        self.agent_location = np.zeros((10, 10))
        self.obstacles = np.zeros((10, 10))
        self.init_target_location()
        self.background = np.copy(self.get_surface())
        self.agent_location = self.init_agent_location()
        self.show_agent = False

        pygame.font.init()
        self.font = pygame.font.SysFont('David', 20)

    def reset(self):
        self.agent_location = self.init_agent_location()
        self.init_target_location()

    def toggle_show_agent(self):
        self.show_agent = not self.show_agent

    def init_agent_location(self):
        x = random.randint(0, 9)
        y = random.randint(0, 9)
        return [x, y]

    def init_target_location(self):

        for i in range(10):
            for j in range(10):
                self.obstacles[i][j] = random.randint(0, 9)

    @staticmethod
    def get_surface():
        return pygame.surfarray.pixels2d(screen)

    def draw(self):
        pygame.surfarray.blit_array(pygame.display.get_surface(), self.background)



        for i in range(10):
            for j in range(10):
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

        if self.show_agent:
            position = self.get_location_vector(self.agent_location)
            pygame.draw.rect(screen, RED, (position[0], position[1], 10, 10))

        pygame.display.flip()

    def get_location_vector(self, location):
        x = location[0] * ROBOT_SIZE
        y = location[1] * ROBOT_SIZE
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
            new_position[1] -= 1
        elif action == 1:
            new_position[0] += 1
        elif action == 2:
            new_position[1] += 1
        elif action == 3:
            new_position[0] -= 1

        if self.is_move_valid(new_position):
            self.agent_location = new_position

        # obs, reward, done
        obs = self.obstacles[self.agent_location[0], self.agent_location[1]]
        print(self.agent_location)
        return obs, 0, False

    def is_move_valid(self, position):

        if position[0] > 9 or position[0] < 0 or position[1] > 9 or position[1] < 0:
            return False

        return True

