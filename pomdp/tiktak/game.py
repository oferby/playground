import numpy as np


class Board:
    def __init__(self):
        self.reset()

        self.masks = [[1, 1, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 1, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 1, 1],
                      [1, 0, 0, 1, 0, 0, 1, 0, 0], [0, 1, 0, 0, 1, 0, 0, 1, 0], [0, 0, 1, 0, 0, 1, 0, 0, 1]]

    def action(self, state):

        if self.states[state] == 0:
            if self.isX:
                self.states[state] = 1
            else:
                self.states[state] = -1
            self.isX = not self.isX
            return True, self.is_winner()
        return False, False

    def reset(self):
        self.states = np.zeros(9)
        self.isX = True

    def is_winner(self):

        for m in self.get_masks():
            if np.sum(np.multiply(self.states, m)) == 3:
                return True
        return False

    def get_masks(self):
        if self.isX:
            return self.masks
        else:
            masks = []
            for m in self.masks:
                masks.append(np.multiply(m, -1))
            return masks

b = Board()
v, w = b.action(0)
assert not w
assert v
