import pygame
import numpy as np

pygame.init()

WHITE = (255, 255, 255)
GREY = (20, 20, 20)
BLACK = (0, 0, 0)
PURPLE = (100, 0, 100)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE_INT = 16777215
BLACK_INT = 0

WORLD_SIZE = (500, 500)
ROBOT_SIZE = 50

screen = pygame.display.set_mode(WORLD_SIZE)
screen.fill(WHITE)

pygame.display.set_caption("Simple Maze")


class World:

    def __init__(self):
        self.agent_location = []
        self.target_location = []
        self.obstacles = []
        self.reset()
        self.background = np.copy(self.get_surface())

        pygame.font.init()
        self.font = pygame.font.SysFont('David', 20)

    def reset(self):
        self.agent_location = [0, 0]
        self.init_target_location()

    def init_target_location(self):
        self.target_location = [9, 9]
        self.obstacles = [[2, 3], [7, 4]]

    @staticmethod
    def get_surface():
        return pygame.surfarray.pixels2d(screen)

    def draw(self):
        pygame.surfarray.blit_array(pygame.display.get_surface(), self.background)

        position = self.get_location_vector(self.agent_location)
        pygame.draw.rect(screen, BLUE, (position[0], position[1], ROBOT_SIZE, ROBOT_SIZE))

        position = self.get_location_vector(self.target_location)
        pygame.draw.rect(screen, RED, (position[0], position[1], ROBOT_SIZE, ROBOT_SIZE))

        for obstacle in self.obstacles:
            position = self.get_location_vector(obstacle)
            pygame.draw.rect(screen, BLACK, (position[0], position[1], ROBOT_SIZE, ROBOT_SIZE))

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
        return 0, 0, self.found_target()

    def is_move_valid(self, position):

        if position[0] > 9 or position[0] < 0 or position[1] > 9 or position[1] < 0:
            return False

        for obstacle in self.obstacles:
            if obstacle[0] == position[0] and obstacle[1] == position[1]:
                return False

        return True

    def found_target(self):
        if self.agent_location[0] == self.target_location[0] and self.agent_location[1] == self.target_location[1]:
            return True
        return False
