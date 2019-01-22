import numpy as np
import pygame

GREEN = 65280

ROBOT_SIZE = 20
STEP_SIZE = 10
WORLD_SIZE = width, height = 600, 400


def add_walls(screen):
    # r = np.random.randint(0,2)
    r = 1
    walls = []
    if r == 0:
        walls.append([0, 100, 300, 5])
        walls.append([450, 0, 5, 300])
        return walls

    elif r == 1:
        walls.append([0, 100, 150, ROBOT_SIZE + 10])
        walls.append([150, 150, 150, ROBOT_SIZE + 10])
        walls.append([250, 200, 150, ROBOT_SIZE + 10])
        walls.append([350, 250, 150, ROBOT_SIZE + 10])
        return walls

    elif r == 2:
        x_ = 150
        y_ = 5
        walls.append([0, 100, x_, y_])
        walls.append([250, 250, x_, y_])

        x_ = 5
        y_ = 150

        walls.append([200, 0, x_, y_])
        walls.append([200, 0, x_, y_])

        return walls

    elif r == 3:
        for i in range(170):
            x = np.random.randint(0, 580)
            x_ = np.random.randint(5, 20)
            y = np.random.randint(0, 380)
            y_ = np.random.randint(5, 20)
            walls.append([x, y, x_, y_])
            pygame.draw.rect(screen, GREEN, pygame.Rect(x, x, ROBOT_SIZE, ROBOT_SIZE))
        return walls


class World:
    def __init__(self, screen, is_mdp=False):
        self.is_mdp = is_mdp
        self.target_location = [550, 350]
        self.surface = pygame.surfarray.pixels2d(screen)
        self.turn = 0
        self.max_turns = 2000
        self.walls = add_walls(screen)

        while True:
            x = np.random.randint(10, 550)
            y = np.random.randint(10, 350)
            if not self.check_surface_for_position(x, y, ROBOT_SIZE):
                self.agent_location = [x, y]
                break

    def get_walls(self):
        return self.walls

    def reset(self):
        return [0, 0, 0, 0]

    def take_action(self, a):

        new_pos = [self.agent_location[0], self.agent_location[1]]
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
            self.agent_location = new_pos

        self.turn += 1
        if self.turn > self.max_turns:
            print('Max turns reached')
            return self.get_obs(), -1, True

        reward, done = self.get_reward()
        return self.get_obs(), reward, done

    def check_valid_action(self, new_location, a):
        if not all([True if x > 1 else False for x in new_location]):
            return False

        if a == 1 and new_location[0] + ROBOT_SIZE > 599:
            return False
        if a == 2 and new_location[1] + ROBOT_SIZE > 399:
            return False

        s = []
        if a == 0:
            # print(new_location[0], new_location[0] + ROBOT_SIZE, new_location[1])
            s = self.surface[new_location[0]: new_location[0] + ROBOT_SIZE, new_location[1]]
            # print(s)

        if a == 1:
            s = self.surface[new_location[0] + ROBOT_SIZE, new_location[1]: new_location[1] + ROBOT_SIZE]
            # print(s)

        if a == 2:
            s = self.surface[new_location[0]:new_location[0] + ROBOT_SIZE,
                new_location[1] + ROBOT_SIZE: new_location[1] + ROBOT_SIZE + 1]
            # print(s)

        if a == 3:
            s = self.surface[new_location[0] - 1:new_location[0], new_location[1]: new_location[1] + ROBOT_SIZE]
            # print(s)

        if self.check_surface(s, ROBOT_SIZE):
            return False

        return True

    def check_surface_for_position(self, x, y, size):
        s = self.surface[x: x + size, y: y + size]
        return self.check_surface(s, size ** 2)

    @staticmethod
    def check_surface(s, size):
        s = np.reshape(s, (size,))
        if any(x == 65280 for x in s):
            # print("found green")
            return True

    def set_surface(self, surface):
        self.surface = surface

    def get_reward(self):
        if self.agent_location[0] == self.target_location[0] and self.target_location[1] == self.agent_location[1]:
            return 100, True
        return -1, False

    def get_obs(self):
        if self.is_mdp:
            return self.surface
        return self.get_partial_obs_for_agent()

    def get_partial_obs_for_agent(self):
        x = int(self.agent_location[0] + ROBOT_SIZE / 2)
        y = int(self.agent_location[1] + ROBOT_SIZE / 2)
        return self.get_partial_obs(x, y)

    def get_partial_obs(self, x, y):
        sensors = [0, 0, 0, 0]
        _x = x
        while _x != 0:
            _x -= 1
            if self.surface[_x, y] == GREEN:
                sensors[3] = x - _x
                break

        _x = x
        while _x != 599:
            _x += 1
            if self.surface[_x, y] == GREEN:
                sensors[1] = _x - x
                break

        _y = y
        while _y != 0:
            _y -= 1
            if self.surface[x, _y] == GREEN:
                sensors[0] = y - _y
                break

        _y = y
        while _y != 399:
            _y += 1
            if self.surface[x, _y] == GREEN:
                sensors[2] = _y - y
                break

        return sensors
