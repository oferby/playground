import abc
import numpy as np
from numpy_ringbuffer import RingBuffer


class AbstractAgent:

    def __init__(self, action_space, state_space):
        self.actions = action_space
        self.states = state_space
        self.memory = RingBuffer(capacity=1000)

    @abc.abstractmethod
    def get_action(self, state):
        pass

    @abc.abstractmethod
    def observe(self, state, action, new_state, reward, done):
        pass


class RandomAgent(AbstractAgent):
    def __init__(self, action_space, state_space):
        super().__init__(action_space, state_space)
        self.cumulative_reward = 0

    def get_action(self, state):
        return np.random.randint(0, self.actions - 1)

    def observe(self, state, action, new_state, reward, done):
        self.cumulative_reward += reward
        state = [round(o, 2) for o in state]
        new_state = [round(o, 2) for o in new_state]
        print(
            'state: {}, \naction: {}, \nnew_state: {}, \nreward: {}, cumulative: {}, done: {}'.format(state, action,
                                                                                                      new_state, reward,
                                                                                                      self.cumulative_reward,
                                                                                                      done))
        print('\n\n')
        if done:
            self.cumulative_reward = 0
