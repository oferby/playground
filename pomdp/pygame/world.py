class World:
    def __init__(self, surface):
        self.agent_location = [50, 50]
        self.target_location = [550, 350]
        self.surface = surface

    def take_action(self, a):
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
            return self.agent_location

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
            print(s)

        if a == 1:
            s = self.surface[new_location[0] + 30, new_location[1]: new_location[1] + 30]
            print(new_location[0] + 30, new_location[1], new_location[1] + 30)
            print(s)

        if self.check_surface(s):
            return False

        return True

    def check_surface(self, s):
        if any(x == 65280 for x in s):
            print("found green")
            return True

    def set_surface(self, surface):
        self.surface = surface
