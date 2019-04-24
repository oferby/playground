from collections import deque
import random
import os
import abc
import sys

import numpy as np
import pygame

import tensorflow as tf
from keras.models import Model, model_from_json, Sequential
from keras.layers import Input, Dense, Add, Multiply
from keras.optimizers import Adam
import keras.backend as K

ACTOR_MODEL = 'actor_model.json'
ACTOR_MODEL_WEIGHTS = 'actor_weights.h5'

CRITIC_MODEL = 'critic_model.json'
CRITIC_MODEL_WEIGHTS = 'critic_weights.h5'


class AbstractAgent:

    def __init__(self, env):
        self.env = env

    @abc.abstractmethod
    def get_action(self, state):
        pass

    @abc.abstractmethod
    def remember(self, state, action, new_state, reward, done):
        pass


# class Agent:
#     def __init__(self, observation_shape, action_shape):
#         self.batch_size = 128
#         self.steps = 0
#         self.epsilon = 1.0
#         self.epsilon_decay = .995
#         self.gamma = .95
#         self.tau = .125
#         self.session = tf.Session()
#         K.set_session(self.session)
#
#         self.actor_input, self.actor = self.create_actor(observation_shape, action_shape[0])
#         _, self.target_actor = self.create_actor(observation_shape, action_shape[0])
#
#         # actor
#         self.actor_critic_grad = tf.placeholder(tf.float32, [None, action_shape[0]])
#         actor_weights = self.actor.trainable_weights
#         self.actor_grads = tf.gradients(self.actor.output, actor_weights, -self.actor_critic_grad)
#         grads = zip(self.actor_grads, actor_weights)
#         self.optimize = tf.train.AdamOptimizer(learning_rate=0.001).apply_gradients(grads)
#
#         # critic
#         self.critic_action_input, self.critic_state_input, self.critic = self.create_critic(observation_shape,
#                                                                                             action_shape)
#         _, _, self.target_critic = self.create_critic(observation_shape, action_shape)
#
#         self.critic_grads = tf.gradients(self.critic.output, self.critic_action_input)
#
#         self.session.run(tf.global_variables_initializer())
#
#         if os.path.isfile(ACTOR_MODEL_WEIGHTS) and os.path.isfile(CRITIC_MODEL_WEIGHTS):
#             self.actor.load_weights(ACTOR_MODEL_WEIGHTS)
#             self.critic.load_weights(CRITIC_MODEL_WEIGHTS)
#
#         self.memory = deque(maxlen=2000)
#
#     # ############################################################################# #
#     #                       Actor Model                                             #
#     # ############################################################################# #
#     @staticmethod
#     def create_actor(input_shape, num_of_actions):
#
#         actor_input = Input(shape=input_shape, name='actor_input')
#         l = Dense(32, activation='tanh')(actor_input)
#         l = Dense(8, activation='tanh')(l)
#         output = Dense(num_of_actions, activation='tanh')(l)
#         actor = Model(inputs=actor_input, outputs=output)
#         adam = Adam(lr=0.001)
#         actor.compile(optimizer=adam, loss='mse')
#
#         return actor_input, actor
#
#     # ############################################################################# #
#     #                       Critic Model                                            #
#     # ############################################################################# #
#     @staticmethod
#     def create_critic(input_shape, action_shape):
#
#         state_input = Input(shape=input_shape)
#         state_h = Dense(24, activation='relu')(state_input)
#         state_h = Dense(48, activation='relu')(state_h)
#
#         action_input = Input(shape=action_shape)
#         action_h = Dense(48, activation='relu')(action_input)
#
#         merged_h = Add()([state_h, action_h])
#         merged_h = Dense(24, activation='relu')(merged_h)
#         output = Dense(1, activation='relu')(merged_h)
#         model = Model(input=[state_input, action_input], output=output)
#         adam = Adam(lr=0.001)
#         model.compile(optimizer=adam, loss='mse')
#         print(model.summary())
#
#         return action_input, state_input, model
#
#     def get_action(self, x):
#
#         if self.epsilon > 0.1:
#             self.epsilon *= self.epsilon_decay
#         if np.random.random() < self.epsilon:
#             action = env.action_space.sample()
#             return np.reshape(action, (1, env.action_space.shape[0]))
#
#         return self.actor.predict(x)
#
#     def add_to_memory(self, current_state, observation, action, reward, done):
#         self.memory.append([current_state, observation, action, reward, done])
#
#     def _train_critic(self, samples):
#         # print('training critic')
#         for sample in samples:
#             current_state, observation, action, reward, done = sample
#
#             # calculate future reward only if not done
#             if not done:
#                 target_action = self.target_actor.predict(observation)
#                 future_reward = self.target_critic.predict([observation, target_action])[0][0]
#                 reward += self.gamma * future_reward
#
#             self.critic.fit([current_state, action], [reward], verbose=0)
#
#         if self.steps % 10 == 0:
#             w = self.actor.get_weights()
#             self.target_actor.set_weights(w)
#             w = self.critic.get_weights()
#             self.target_critic.set_weights(w)
#             print('weights updated')
#
#     def _train_actor(self, samples):
#         # print('training actor')
#         for sample in samples:
#             current_state, observation, action, reward, done = sample
#             predicted_action = self.actor.predict(current_state)
#             grads = self.session.run(self.critic_grads, feed_dict={
#                 self.critic_state_input: current_state,
#                 self.critic_action_input: predicted_action
#             })[0]
#
#             self.session.run(self.optimize, feed_dict={
#                 self.actor_input: current_state,
#                 self.actor_critic_grad: grads
#             })
#
#     def save(self):
#
#         self.actor.save_weights(ACTOR_MODEL_WEIGHTS)
#         self.critic.save_weights(CRITIC_MODEL_WEIGHTS)
#
#     def train(self):
#
#         if len(self.memory) < self.batch_size:
#             return
#
#         # for i in range(4):
#         samples = random.sample(self.memory, self.batch_size)
#         self._train_critic(samples)
#         self._train_actor(samples)
#         self.steps += 1
#
#         self.save()


class ActorCriticAgentContinuous(AbstractAgent):
    def __init__(self, env):
        super(ActorCriticAgentContinuous, self).__init__(env)
        self.session = tf.Session()
        K.set_session(self.session)

        self.learning_rate = 0.001
        self.epsilon = 1.
        self.epsilon_decay = .995
        self.epsilon_min = .01
        self.gamma = .95
        self.step = 0
        self.batch_size = 32
        self.memory = deque(maxlen=2000)

        self.actor_input, self.actor = self.create_actor()
        _, self.actor_target = self.create_actor()

        print(self.actor.summary())

        self.actor_critic_grad = tf.placeholder(tf.float32, [None, self.env.action_space.shape[0]])

        actor_model_weights = self.actor.trainable_weights
        self.actor_grads = tf.gradients(self.actor.output, actor_model_weights, -self.actor_critic_grad)
        grads = zip(self.actor_grads, actor_model_weights)
        self.optimize = tf.train.AdamOptimizer(self.learning_rate).apply_gradients(grads)

        self.critic_state_input, self.critic_action_input, self.critic = self.create_critic()
        _, _, self.critic_target = self.create_critic()

        self.critic_grads = tf.gradients(self.critic.output, self.critic_action_input)

        print(self.critic.summary())

        self.session.run(tf.global_variables_initializer())

    def create_actor(self):
        state_input = Input(shape=self.env.observation_space.shape)
        h = Dense(24, activation='tanh')(state_input)
        h = Dense(48, activation='tanh')(h)
        h = Dense(24, activation='tanh')(h)
        output = Dense(self.env.action_space.shape[0], activation='tanh')(h)

        model = Model(input=state_input, output=output)
        adam = Adam(lr=self.learning_rate)
        model.compile(loss='mse', optimizer=adam)
        return state_input, model

    def create_critic(self):
        state_input = Input(shape=self.env.observation_space.shape)
        s_h = Dense(24, activation='relu')(state_input)
        s_h = Dense(48, activation='relu')(s_h)

        action_input = Input(shape=self.env.action_space.shape)
        # a_h = Dense(24, activation='relu')(action_input)
        a_h = Dense(48, activation='relu')(action_input)

        merged = Add()([s_h, a_h])
        h = Dense(24, activation='relu')(merged)
        output = Dense(1, activation='relu')(h)
        model = Model(input=[state_input, action_input], output=output)

        adam = Adam(lr=self.learning_rate)
        model.compile(loss='mse', optimizer=adam)
        return state_input, action_input, model

    def train(self):

        if len(self.memory) < self.batch_size:
            return

        print('training...')
        samples = random.sample(self.memory, self.batch_size)
        self._train_critic(samples)
        self._train_actor(samples)

        self.step += 1
        if self.step > 100:
            self._update_actor_target()
            self._update_critic_target()
            self.step = 0

    def _train_actor(self, samples):

        for sample in samples:
            state, action, new_state, reward, done = sample
            predicted_action = self.actor.predict(state)
            grads = self.session.run(self.critic_grads, feed_dict={
                self.critic_state_input: state,
                self.critic_action_input: predicted_action
            })

            print('grads', grads)

            self.session.run(self.optimize, feed_dict={
                self.actor_input: state,
                self.critic_grads: grads
            })

    def _train_critic(self, samples):

        for sample in samples:
            state, action, new_state, reward, done = sample
            if not done:
                new_state = new_state.reshape((1, self.env.observation_space.shape[0]))
                target_action = self.actor_target.predict(new_state)
                future_reward = self.critic_target.predict([new_state, target_action])[0][0]
                reward += self.gamma * future_reward

            self.critic.fit([state, action], reward, verbose=0)

    def _update_actor_target(self):
        self.actor_target.set_weights(self.actor.get_weights())

    def _update_critic_target(self):
        self.critic_target.set_weights(self.critic.get_weights())

    def save(self):
        pass

    def get_action(self, state):

        if self.epsilon > self.epsilon_min and random.random() < self.epsilon:
            self.epsilon *= self.epsilon_decay
            # print('random')
            return self.env.action_space.sample()

        # print('greedy')
        state = state.reshape((1, self.env.observation_space.shape[0]))
        return self.actor.predict(state)[0]

    def remember(self, state, action, new_state, reward, done):

        state = np.reshape(state, (1, self.env.observation_space.shape[0]))
        action = np.reshape(action, (1, self.env.action_space.shape[0]))
        new_state = np.reshape(new_state, (1, self.env.observation_space.shape[0]))
        reward = np.reshape(reward, (1, 1))

        self.memory.append([state, action, new_state, reward, done])


class ActorAgent(AbstractAgent):

    def __init__(self, env):
        super(ActorAgent, self).__init__(env)

        self.learning_rate = 0.001
        self.epsilon = 1.
        # self.epsilon = .001
        self.epsilon_decay = .995
        self.epsilon_min = .1
        self.gamma = .95
        self.step = 0
        self.batch_size = 128
        self.memory = deque(maxlen=20000)

        self.actor_input, self.actor = self.create_actor()
        _, self.actor_target = self.create_actor()

    def create_actor(self):
        state_input = Input(shape=self.env.observation_space.shape)
        h = Dense(24, activation='relu')(state_input)
        h = Dense(48, activation='relu')(h)
        h = Dense(24, activation='relu')(h)
        output = Dense(self.env.action_space.n)(h)

        model = Model(input=state_input, output=output)
        adam = Adam(lr=self.learning_rate)
        model.compile(loss='mse', optimizer=adam)

        if os.path.isfile(self.__class__.__name__ + '_' + ACTOR_MODEL_WEIGHTS):
            print('loading weights from file')
            model.load_weights(self.__class__.__name__ + '_' + ACTOR_MODEL_WEIGHTS)

        return state_input, model

    def remember(self, state, action, new_state, reward, done):
        state = np.reshape(state, (1, self.env.observation_space.shape[0]))
        new_state = np.reshape(new_state, (1, self.env.observation_space.shape[0]))

        self.memory.append([state, action, new_state, reward, done])

    def get_action(self, state):

        r = random.random()
        if r < self.epsilon:
            if self.epsilon > self.epsilon_min:
                self.epsilon *= self.epsilon_decay
            # print('random')
            return self.env.action_space.sample()

        # print('greedy')
        state = state.reshape((1, self.env.observation_space.shape[0]))
        action = self.actor.predict(state)
        return np.argmax(action[0])

    def train(self):

        if len(self.memory) < self.batch_size:
            return

        samples = random.sample(self.memory, self.batch_size)
        # samples.append(self.memory[-1])

        states = []
        q_states = []
        for sample in samples:
            state, action, new_state, reward, done = sample

            if not done:
                future_reward = self.actor_target.predict(new_state)[0]
                double_dqn_fix = self.actor.predict(new_state)[0]
                reward += self.gamma * future_reward[np.argmax(double_dqn_fix)]
                # reward += self.gamma * np.average(future_reward)

            q_state = self.actor.predict(state)[0]
            q_state[action] = reward
            q_state = np.reshape(q_state, (1, self.env.action_space.n))
            states.append(state)
            q_states.append(q_state)
        q_states = np.reshape(q_states, (self.batch_size, self.env.action_space.n))
        states = np.reshape(states, (self.batch_size, self.env.observation_space.shape[0]))
        self.actor.fit(states, q_states, verbose=0, epochs=1)

        self.save()
        self.step+=1

        if self.step > 20:
            self.actor_target.set_weights(self.actor.get_weights())
            self.step = 0

    def save(self):
        self.actor.save_weights(self.__class__.__name__ + '_' + ACTOR_MODEL_WEIGHTS)


class ActorAgent1(AbstractAgent):

    def __init__(self, env):
        super(ActorAgent1, self).__init__(env)

        self.learning_rate = 0.001
        self.epsilon = 1.
        # self.epsilon = .001
        self.epsilon_decay = .995
        self.epsilon_min = .1
        self.gamma = .95
        self.step = 0
        self.batch_size = 128
        self.trajectory = 0
        self.memory = deque(maxlen=20000)

        self.actor_input, self.actor = self.create_actor()
        _, self.actor_target = self.create_actor()

    def create_actor(self):
        new_shape = self.env.observation_space.shape[0] + 1
        new_shape = (new_shape, )
        state_input = Input(shape=new_shape)
        h = Dense(24, activation='relu')(state_input)
        h = Dense(48, activation='relu')(h)
        h = Dense(24, activation='relu')(h)
        output = Dense(self.env.action_space.n)(h)

        model = Model(input=state_input, output=output)
        adam = Adam(lr=self.learning_rate)
        model.compile(loss='mse', optimizer=adam)

        if os.path.isfile(self.__class__.__name__ + '_' + ACTOR_MODEL_WEIGHTS):
            print('loading weights from file')
            model.load_weights(self.__class__.__name__ + '_' + ACTOR_MODEL_WEIGHTS)

        return state_input, model

    def remember(self, state, action, new_state, reward, done):

        state = np.concatenate((state, [self.trajectory]))
        state = np.reshape(state, (1, self.env.observation_space.shape[0] + 1))

        new_state = np.concatenate((new_state, [self.trajectory + 1]))
        new_state = np.reshape(new_state, (1, self.env.observation_space.shape[0] + 1))

        self.memory.append([state, action, new_state, reward, done])

        if done:
            self.trajectory = 0

    def get_action(self, state):

        self.trajectory += 1

        r = random.random()
        if r < self.epsilon:
            if self.epsilon > self.epsilon_min:
                self.epsilon *= self.epsilon_decay
            # print('random')
            return self.env.action_space.sample()

        # print('greedy')
        state = np.concatenate((state, [self.trajectory]))
        state = state.reshape((1, self.env.observation_space.shape[0] + 1))
        action = self.actor.predict(state)
        return np.argmax(action[0])

    def train(self):

        if len(self.memory) < self.batch_size:
            return

        states = []
        q_states = []

        _, _, _, reward, _ = self.memory[-1]
        if reward == 100:
            samples = random.sample(self.memory, self.batch_size - 1)
            samples.append(self.memory[-1])
        else:
            samples = random.sample(self.memory, self.batch_size)

        for sample in samples:
            state, action, new_state, reward, done = sample

            if not done:
                future_reward = self.actor_target.predict(new_state)[0]
                double_dqn_fix = self.actor.predict(new_state)[0]
                reward += self.gamma * future_reward[np.argmax(double_dqn_fix)]
                # reward += self.gamma * np.average(future_reward)

            q_state = self.actor.predict(state)[0]
            q_state[action] = reward
            q_state = np.reshape(q_state, (1, self.env.action_space.n))
            states.append(state)
            q_states.append(q_state)
        q_states = np.reshape(q_states, (self.batch_size, self.env.action_space.n))
        states = np.reshape(states, (self.batch_size, self.env.observation_space.shape[0] + 1))
        self.actor.fit(states, q_states, verbose=0, epochs=1)

        self.save()
        self.step += 1

        if self.step > 20:
            self.actor_target.set_weights(self.actor.get_weights())
            self.step = 0

    def save(self):
        self.actor.save_weights(self.__class__.__name__ + '_' + ACTOR_MODEL_WEIGHTS)


class KeyboardAgent(AbstractAgent):

    def __init__(self, env):
        pygame.init()
        BLACK = (0, 0, 0)
        WIDTH = 100
        HEIGHT = 100
        windowSurface = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)



        self.key_value = 0

    def remember(self, state, action, new_state, reward, done):
        pass

    def get_action(self, obs):

        for event in pygame.event.get():
            # print('event:', event)
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYUP:
                self.key_value = 0

            elif event.type == pygame.KEYDOWN:
                k = event.key
                # up
                if k == 273:
                    self.key_value = 2
                # down
                elif k == 274:
                    self.key_value = 0
                # right
                elif k == 275:
                    self.key_value = 3
                # left
                elif k == 276:
                    self.key_value = 1

        return self.key_value

    def train(self):
        pass
