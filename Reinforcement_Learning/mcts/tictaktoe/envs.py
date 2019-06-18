import numpy as np
import abc


def make():
    return Simple()


class AbstractEnv:

    @abc.abstractmethod
    def get_action_space(self):
        pass

    @abc.abstractmethod
    def get_state_space(self):
        pass

    @abc.abstractmethod
    def reset(self):
        pass

    @abc.abstractmethod
    def step(self, action):
        pass

    @abc.abstractmethod
    def render(self):
        pass


class Simple(AbstractEnv):

    def __init__(self):
        self.board = None
        self.reset()
        self.x_turn = True

    def get_action_space(self):
        return 9

    def get_state_space(self):
        return 9

    def reset(self):
        self.board = np.zeros((3, 3))
        self.x_turn = True
        return self._get_state()

    def _get_state(self):
        return np.copy(self.board.reshape((9)))

    def step(self, action):

        turn = 1 if self.x_turn else -1

        b = self.board.reshape((9))

        if b[action] == 0:

            b[action] = turn
            self.board = b.reshape((3, 3))

            self.x_turn = not self.x_turn

            done, reward = self.check_if_done(turn)
            info = ['valid']
        else:
            done = False
            reward = 0
            info = ['not-valid']

        state = self._get_state()

        return state, reward, done, info

    def check_if_done(self, turn):

        done = 0 not in self.board

        val = turn * 3
        for i in range(3):
            if sum(self.board[i, :]) == val:
                return True, 1

            if sum(self.board[:, i]) == val:
                return True, 1

        i = np.identity(3)

        s = np.sum(self.board * i)
        if s == val:
            return True, 1

        i = np.flip(i, 1)

        s = np.sum(self.board * i)
        if s == val:
            return True, 1

        if not done:
            return done, 0

        return True, 0

    def render(self):

        for i in range(9):
            b = self.board.reshape((9))
            if b[i] == 1:
                mark = 'X'
            elif b[i] == -1:
                mark = 'O'
            else:
                mark = '_'

            if i % 3 == 0:
                print()

            print('\t{}'.format(mark), end='')

        print()
