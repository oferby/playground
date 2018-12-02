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
WHITE_INT = 16777215
BLACK_INT = 0

ROBOT_SIZE = 20
STEP_SIZE = 10

WORLD_SIZE = (701, 701)
screen = pygame.display.set_mode(WORLD_SIZE)

pygame.display.set_caption("Maze Generator")

done = False
show_agent = False

width = 50
cols = int(WORLD_SIZE[0] / width)
rows = int(WORLD_SIZE[1] / width)

stack = []


class Cell:
    def __init__(self, x, y, grid):
        global width
        self.x = x * width
        self.y = y * width
        self.grid = grid

        self.visited = False
        self.current = False

        self.walls = [True, True, True, True]  # top , right , bottom , left

        # neighbors
        self.neighbors = []

        self.top = 0
        self.right = 0
        self.bottom = 0
        self.left = 0

        self.next_cell = 0

    def draw(self):
        if self.current:
            pygame.draw.rect(screen, WHITE, (self.x, self.y, width, width))
        elif self.visited:
            pygame.draw.rect(screen, WHITE, (self.x, self.y, width, width))

            if self.walls[0]:
                pygame.draw.line(screen, BLACK, (self.x, self.y), ((self.x + width), self.y), 1)  # top
            if self.walls[1]:
                pygame.draw.line(screen, BLACK, ((self.x + width), self.y), ((self.x + width), (self.y + width)),
                                 1)  # right
            if self.walls[2]:
                pygame.draw.line(screen, BLACK, ((self.x + width), (self.y + width)), (self.x, (self.y + width)),
                                 1)  # bottom
            if self.walls[3]:
                pygame.draw.line(screen, BLACK, (self.x, (self.y + width)), (self.x, self.y), 1)  # left

    def checkNeighbors(self):
        # print("Top; y: " + str(int(self.y / width)) + ", y - 1: " + str(int(self.y / width) - 1))
        if int(self.y / width) - 1 >= 0:
            self.top = self.grid[int(self.y / width) - 1][int(self.x / width)]
        # print("Right; x: " + str(int(self.x / width)) + ", x + 1: " + str(int(self.x / width) + 1))
        if int(self.x / width) + 1 <= cols - 1:
            self.right = self.grid[int(self.y / width)][int(self.x / width) + 1]
        # print("Bottom; y: " + str(int(self.y / width)) + ", y + 1: " + str(int(self.y / width) + 1))
        if int(self.y / width) + 1 <= rows - 1:
            self.bottom = self.grid[int(self.y / width) + 1][int(self.x / width)]
        # print("Left; x: " + str(int(self.x / width)) + ", x - 1: " + str(int(self.x / width) - 1))
        if int(self.x / width) - 1 >= 0:
            self.left = self.grid[int(self.y / width)][int(self.x / width) - 1]
        # print("--------------------")

        if self.top != 0:
            if not self.top.visited:
                self.neighbors.append(self.top)
        if self.right != 0:
            if not self.right.visited:
                self.neighbors.append(self.right)
        if self.bottom != 0:
            if not self.bottom.visited:
                self.neighbors.append(self.bottom)
        if self.left != 0:
            if not self.left.visited:
                self.neighbors.append(self.left)

        if len(self.neighbors) > 0:
            self.next_cell = self.neighbors[random.randrange(0, len(self.neighbors))]
            return self.next_cell
        else:
            return False


class World:

    def __init__(self):
        self.agent_location = []
        self.create()
        self.surface = pygame.surfarray.pixels2d(screen)
        self.target_location = [660, 660]
        self.turn = 0
        self.max_turns = 2000
        self.is_mdp = False

    def get_observation(self):
        pass

    def draw(self, old_location=None):
        if old_location:
            pygame.draw.rect(screen, WHITE, (old_location[0], old_location[1], ROBOT_SIZE, ROBOT_SIZE))
        pygame.draw.rect(screen, BLUE, (self.agent_location[0], self.agent_location[1], ROBOT_SIZE, ROBOT_SIZE))
        pygame.display.flip()

    def take_action(self, a):

        new_pos = [x for x in self.agent_location]

        # up
        if a == 0:
            new_pos[1] = new_pos[1] - STEP_SIZE
        # right
        elif a == 1:
            new_pos[0] = new_pos[0] + STEP_SIZE
        # down
        elif a == 2:
            new_pos[1] = new_pos[1] + STEP_SIZE
        # left
        elif a == 3:
            new_pos[0] = new_pos[0] - STEP_SIZE

        if self.check_valid_action(new_pos, a):
            old_location = self.agent_location
            self.agent_location = new_pos
            self.draw(old_location)

        self.turn += 1
        if self.turn > self.max_turns:
            print('Max turns reached')
            return self.get_obs(), -1, True

        reward, done = self.get_reward()
        return self.get_obs(), reward, done

    def get_obs(self):
        if self.is_mdp:
            return self.surface
        return self.get_partial_obs_for_agent()

    def get_reward(self):
        if self.agent_location[0] == self.target_location[0] and self.target_location[1] == self.agent_location[1]:
            return 100, True
        return -1, False

    def check_valid_action(self, new_location, a):
        if not all([True if x > 1 else False for x in new_location]):
            return False

        if a == 1 and new_location[0] + ROBOT_SIZE > WORLD_SIZE[0]:
            return False
        if a == 2 and new_location[1] + ROBOT_SIZE > WORLD_SIZE[1]:
            return False

        s = []
        if a == 0:
            # print(new_location[0], new_location[0] + ROBOT_SIZE, new_location[1])
            s = self.surface[new_location[0]: new_location[0] + ROBOT_SIZE,
                new_location[1]: new_location[1] + STEP_SIZE]
            # print(s)

        elif a == 1:
            s = self.surface[new_location[0] + ROBOT_SIZE - STEP_SIZE:new_location[0] + ROBOT_SIZE,
                new_location[1]: new_location[1] + ROBOT_SIZE]
            # print(s)

        elif a == 2:
            s = self.surface[new_location[0]:new_location[0] + ROBOT_SIZE,
                new_location[1] + ROBOT_SIZE - STEP_SIZE: new_location[1] + ROBOT_SIZE]
            # print(s)

        elif a == 3:
            s = self.surface[new_location[0] :new_location[0] + STEP_SIZE, new_location[1]: new_location[1] + ROBOT_SIZE]
            # print(s)

        if self.check_surface(s, np.size(s)):
            return False

        return True

    def check_surface_for_position(self, x, y, size):
        s = self.surface[x: x + size, y: y + size]
        return self.check_surface(s, size ** 2)

    @staticmethod
    def check_surface(s, size):
        s = np.reshape(s, (size,))
        if any(x != WHITE_INT for x in s):
            # print("found black")
            return True

    def get_partial_obs_for_agent(self):
        x = int(self.agent_location[0] + ROBOT_SIZE / 2)
        y = int(self.agent_location[1] + ROBOT_SIZE / 2)
        return self.get_partial_obs(x, y)

    def get_partial_obs(self, x, y):
        sensors = [0, 0, 0, 0]
        _x = x
        while _x != 0:
            _x -= 1
            if self.surface[_x, y] == BLACK_INT:
                sensors[3] = x - _x
                break

        _x = x
        while _x != 599:
            _x += 1
            if self.surface[_x, y] == BLACK_INT:
                sensors[1] = _x - x
                break

        _y = y
        while _y != 0:
            _y -= 1
            if self.surface[x, _y] == BLACK_INT:
                sensors[0] = y - _y
                break

        _y = y
        while _y != 399:
            _y += 1
            if self.surface[x, _y] == BLACK_INT:
                sensors[2] = _y - y
                break

        return sensors

    def removeWalls(self, current_cell, next_cell):
        x = int(current_cell.x / width) - int(next_cell.x / width)
        y = int(current_cell.y / width) - int(next_cell.y / width)
        if x == -1:  # right of current
            current_cell.walls[1] = False
            next_cell.walls[3] = False
        elif x == 1:  # left of current
            current_cell.walls[3] = False
            next_cell.walls[1] = False
        elif y == -1:  # bottom of current
            current_cell.walls[2] = False
            next_cell.walls[0] = False
        elif y == 1:  # top of current
            current_cell.walls[0] = False
            next_cell.walls[2] = False

    def create(self):
        grid = []

        for y in range(rows):
            grid.append([])
            for x in range(cols):
                grid[y].append(Cell(x, y, grid))

        current_cell = grid[0][0]
        next_cell = 0

        # -------- Main Program Loop -----------
        while not done:
            # --- Main event loop

            screen.fill(GREY)

            current_cell.visited = True
            current_cell.current = True

            for y in range(rows):
                for x in range(cols):
                    grid[y][x].draw()

            next_cell = current_cell.checkNeighbors()

            if next_cell:
                current_cell.neighbors = []

                stack.append(current_cell)

                self.removeWalls(current_cell, next_cell)

                current_cell.current = False

                current_cell = next_cell

            elif len(stack) > 0:
                current_cell.current = False
                current_cell = stack.pop()

            elif len(stack) == 0:
                break

        self.init_agent_location()
        self.draw()

    def init_agent_location(self):
        self.agent_location = [5, 5]
