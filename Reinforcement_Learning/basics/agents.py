import abc
import numpy as np
import random
import os


class AbstractAgent:

    def __init__(self, action_space, state_space):
        self.actions = action_space
        self.states = state_space

    @abc.abstractmethod
    def get_action(self, state):
        pass

    @abc.abstractmethod
    def remember(self, state, action, new_state, reward, done):
        pass


class RandomAgent(AbstractAgent):

    def get_action(self, state):
        return np.random.randint(0, self.actions - 1)

    def remember(self, state, action, new_state, reward, done):
        print(
            'state: {}, action: {}, new_state: {}, reward: {}, done: {}'.format(state, action, new_state, reward, done))
        print('\n\n\n')


class SimpleAgent(AbstractAgent):

    def __init__(self, action_space, state_space):
        super(SimpleAgent, self).__init__(action_space, state_space)
        self.world = np.zeros((state_space, action_space))
        self.epsilon = 1
        self.decay = .7

    def get_action(self, state):
        if np.random.random() < self.epsilon:
            self.epsilon *= self.decay
            return np.random.randint(0, self.actions - 1)

        return np.argmax(self.world[state])

    def remember(self, state, action, new_state, reward, done, print_result=False):
        if done:
            self.world[state, action] = reward
        else:
            self.world[state, action] = reward + max(self.world[new_state])


class SimpleRL(AbstractAgent):

    def __init__(self, action_space, state_space):

        self.MODEL_WEIGHTS = 'model.h5'

        super(SimpleRL, self).__init__(action_space, state_space)

        from collections import deque
        from tensorflow.contrib.keras.api.keras.utils import to_categorical

        self.epsilon = 1
        self.epsilon_decay = .9997
        self.steps = 0
        self.gamma = .9

        self.memory = deque(maxlen=2000)

        self.to_categorical = to_categorical

        self.model = self._get_model()
        self.target_model = self._get_model()

        self.training_steps = 0

    def _get_model(self):

        from tensorflow.contrib.keras.api.keras.layers import Dense, Input
        from tensorflow.contrib.keras.api.keras.models import Model
        from tensorflow.train import AdamOptimizer

        # tf.enable_eager_execution()

        state_input = Input(shape=(1, self.states))
        h = Dense(24)(state_input)
        h = Dense(48)(h)
        actions = Dense(self.actions)(h)
        model = Model(inputs=state_input, outputs=actions)
        adam = AdamOptimizer(learning_rate=0.001)
        model.compile(optimizer=adam, loss='mse')

        if os.path.isfile(self.MODEL_WEIGHTS):
            print('loading weights from file')
            model.load_weights(self.MODEL_WEIGHTS)
            self.epsilon = 0.01

        print(model.summary())

        return model

    def get_action(self, state):

        if self.epsilon > np.random.random():
            if self.epsilon > 0.01:
                self.epsilon *= self.epsilon_decay
            print('using random')
            return np.random.randint(0, self.actions - 1)

        actions = self._get_action_values(state, self.model)
        taking_action = np.argmax(actions)
        print('state: {},  actions: {}, taking: {}'.format(state, actions, taking_action))

        return taking_action

    def _get_action_values(self, state, model):

        one_hot = self.to_categorical(state, num_classes=self.states)
        actions = model.predict(np.reshape(one_hot, (1, 1, self.states)))
        return actions[0][0]

    def remember(self, state, action, new_state, reward, done):

        self.memory.append([state, action, new_state, reward, done])
        self.steps += 1
        if self.steps % 100 == 0:
            self._train()

    def _train(self):
        # self.steps = 0
        training_states = []
        training_values = []
        batch_size = 32
        samples = random.sample(self.memory, batch_size)

        for sample in samples:
            state, action, new_state, reward, done = sample

            values = self._get_action_values(state, self.model)

            if not done:
                new_state_values = self._get_action_values(new_state, self.target_model)
                reward = reward + self.gamma * max(new_state_values)

            values[action] = reward
            # print("after {}: {}".format(state, values))
            one_host_state = self.to_categorical(state, num_classes=self.states)
            training_states.append(one_host_state)
            training_values.append(values)
        x = np.reshape(np.asanyarray(training_states), (batch_size, 1, self.states))
        y = np.reshape(np.asanyarray(training_values), (batch_size, 1, self.actions))
        # print('shapes: x:{} y:{}'.format(x.shape, y.shape))
        self.model.fit(x, y, epochs=3, verbose=0)
        self.model.save_weights(self.MODEL_WEIGHTS)

        # we update the Target network once every 10 training step of the active network
        self.training_steps += 1
        if self.training_steps > 10:
            self.target_model.set_weights(self.model.get_weights())
            self.training_steps = 0
