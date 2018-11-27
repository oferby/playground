import numpy as np

GREEN = 65280

ROBOT_SIZE = 20
STEP_SIZE = 10
WORLD_SIZE = width, height = 600, 400


class World:
    def __init__(self, surface, is_mdp=False):
        self.is_mdp = is_mdp
        self.agent_location = [50, 50]
        self.target_location = [550, 350]
        self.surface = surface
        self.turn = 0
        self.max_turns = 2000
        self.walls = []
        self.add_walls()

    def add_walls(self):
        self.walls.append([0, 100, 300, 5])
        self.walls.append([450, 0, 5, 300])

    def get_walls(self):
        return self.walls

    def reset(self):
        self.agent_location = [50, 50]
        self.target_location = [550, 350]
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
