import sys
import numpy as np

sys.path.insert(0, "./")

import agents

LEFT = 0
RIGHT = 1
DOWN = 2
UP = 3


class Environment:
    def __init__(self):
        self.states = 100
        self.actions = 4
        self.state = None
        self.done = False
        self.pits = None
        self.wins = [0, 99]

        self.pits = [11, 24, 48, 66]
        # for i in range(4):
        #     self.pits.append(np.random.randint(1, 99))

    def reset(self):

        ok = False
        while not ok:
            s = np.random.randint(100)
            if s not in self.pits and s not in self.wins:
                ok = True
                self.state = s

        self.done = False

        return self.state

    def is_valid_state(self, state):

        if state < 0 or state > self.states - 1:
            return False

        board_size = np.sqrt(self.states)

        if state // board_size == self.state // board_size:
            # same raw
            if state % board_size == (self.state % board_size) + 1 or state % board_size == (
                    self.state % board_size) - 1:
                return True
            else:
                return False

        if state % board_size == self.state % board_size:
            return True

        return False

    def step(self, action):

        if action == LEFT:
            ns = self.state - 1
        elif action == RIGHT:
            ns = self.state + 1
        elif action == DOWN:
            ns = self.state - int(np.sqrt(self.states))
        else:
            # UP
            ns = self.state + int(np.sqrt(self.states))

        if not self.is_valid_state(ns):
            return self.state, -1, self.done

        self.state = ns

        return self.state, self._get_reward(), self.done

    def _get_reward(self):

        if self.state in self.wins:
            self.done = True
            return 100

        if self.state in self.pits:
            self.done = True
            return -100

        return -1

    def render(self):
        board = ["" for i in range(100)]

        for p in self.pits:
            board[p] = 'O'
        board[99] = 'X'
        board[0] = 'X'
        board[self.state] = '$'
        board = np.reshape(board, (10, 10))
        for i in board:
            print(i)


def main():
    render = False

    env = Environment()
    # agent = agents.SimpleAgent(env.actions, env.states)
    agent = agents.SimpleRL(env.actions, env.states)
    max_loose = 0

    for n in range(5000):
        print('starting session {}'.format(n))
        state = env.reset()
        if render:
            env.render()

        done = False
        while not done:
            action = agent.get_action(state)
            new_state, reward, done = env.step(action)
            agent.remember(state, action, new_state, reward, done)

            if render:
                print(
                    'state: {}, action: {}, new_state: {}, reward: {}, done: {}'.format(state, action,
                                                                                        new_state,
                                                                                        reward,
                                                                                        done))
                print('\n\n')
                env.render()

            state = new_state

        if reward == 100:
            print('win')
        else:
            print("loose")
            max_loose = n

    print('max loose: {}'.format(max_loose))


if __name__ == '__main__':
    main()
