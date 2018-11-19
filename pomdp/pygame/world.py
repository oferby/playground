import numpy as np

GREEN = 0, 255, 0


class World:
    def __init__(self, surface):

        self.agent_location = [50, 50]
        self.target_location = [550, 350]
        self.surface = surface
        self.turn = 0
        self.max_turns = 2000
        self.walls = []
        self.walls.append([0, 100, 300, 5])

    def get_walls(self):
        return self.walls

    def reset(self):
        self.agent_location = [50, 50]
        self.target_location = [550, 350]

    def take_action(self, a):
        self.turn += 1
        if self.turn > self.max_turns:
            print('Max turns reached')
            return None, None, True

        new_pos = [self.agent_location[0], self.agent_location[1]]
        if a == 0:
            new_pos[1] = new_pos[1] - 10
        elif a == 1:
            new_pos[0] = new_pos[0] + 10
        elif a == 2:
            new_pos[1] = new_pos[1] + 10
        elif a == 3:
            new_pos[0] = new_pos[0] - 10

        if self.check_valid_action(new_pos, a):
            self.agent_location = new_pos

        reward, done = self.get_reward()
        return self.get_obs(), reward, done

    def check_valid_action(self, new_location, a):
        if not all([True if x > 1 else False for x in new_location]):
            return False

        if a == 1 and new_location[0] + 30 > 599:
            return False
        if a == 2 and new_location[1] + 30 > 399:
            return False

        s = []
        if a == 0:
            print(new_location[0], new_location[0] + 30, new_location[1])
            s = self.surface[new_location[0]: new_location[0] + 30, new_location[1]]
            # print(s)

        if a == 1:
            s = self.surface[new_location[0] + 30, new_location[1]: new_location[1] + 30]
            # print(s)

        if a == 2:
            s = self.surface[new_location[0]:new_location[0] + 30, new_location[1] + 30: new_location[1] + 31]
            # print(s)

        if a == 3:
            s = self.surface[new_location[0] - 1:new_location[0], new_location[1]: new_location[1] + 30]
            # print(s)

        if self.check_surface(s):
            return False

        return True

    def check_surface(self, s):
        s = np.reshape(s, (30,))
        if any(x == 65280 for x in s):
            print("found green")
            return True
        # if any(x == 16711680 for x in s):
        #     print("found red")
        #     return True

    def set_surface(self, surface):
        self.surface = surface

    def get_reward(self):
        if self.agent_location[0] == self.target_location[0] and self.target_location[1] == self.agent_location[1]:
            return 100, True
        return -1, False

    def get_obs(self):
        sensors = [0, 0, 0, 0]
        x = self.agent_location[0] + 15
        y = self.agent_location[1] + 15
        _x = x
        _y = y

        # while _y != 0:

        # while _x != 0:
        #     if self.surface[_x, y] == GREEN:
        #         sensors[1] = x - _x
        #         break
        #     _x -= 1

        return sensors
