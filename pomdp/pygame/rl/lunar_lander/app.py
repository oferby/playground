import gym

env = gym.make('LunarLanderContinuous-v2')

import tensorflow as tf
from keras.models import Model, model_from_json
from keras.layers import Input, Dense, Add
from keras.optimizers import Adam
import keras.backend as K

import os
import numpy as np
import collections

KERAS_MODEL = './keras_model.json'
KERAS_MODEL_WEIGHTS = 'keras_model_weights.h5'


class Agent:
    def __init__(self, input_shape, action_shape):

        self.epsilon = 1.0
        self.epsilon_decay = .995
        self.gamma = .95
        self.tau = .125
        self.session = tf.Session()
        K.set_session(self.session)

        self.actor_input, self.actor = self.create_actor(input_shape, action_shape[0])

        self.action_input, self.state_input, self.critic = self.create_critic(input_shape, action_shape)

        self.memory = collections.deque(maxlen=2000)

    # ############################################################################# #
    #                       Actor Model                                             #
    # ############################################################################# #

    def create_actor(self, input_shape, num_of_actions, save=False):
        if os.path.isfile(KERAS_MODEL) and save:
            json_file = open(KERAS_MODEL, 'r')
            actor = model_from_json(json_file.read())
            actor.load_weights(KERAS_MODEL_WEIGHTS)
            actor_input = actor.get_layer('actor_input')
        else:
            actor_input = Input(shape=input_shape, name='actor_input')
            l = Dense(32, activation='tanh')(actor_input)
            l = Dense(8, activation='tanh')(l)
            output = Dense(num_of_actions, activation='tanh')(l)
            actor = Model(inputs=actor_input, outputs=output)
            adam = Adam(lr=0.001)
            actor.compile(optimizer=adam, loss='mse')
            actor.save_weights(KERAS_MODEL_WEIGHTS)

            json_model = actor.to_json()
            with open(KERAS_MODEL, 'w') as json_file:
                json_file.write(json_model)

        return actor_input, actor

    # ############################################################################# #
    #                       Critic Model                                            #
    # ############################################################################# #

    def create_critic(self, input_shape, action_shape):

        state_input = Input(shape=input_shape)
        state_h = Dense(24, activation='relu')(state_input)
        state_h = Dense(48, activation='relu')(state_h)

        action_input = Input(shape=action_shape)
        action_h = Dense(48, activation='relu')(action_input)

        merged_h = Add()([state_h, action_h])
        merged_h = Dense(24, activation='relu')(merged_h)
        output = Dense(1, activation='relu')(merged_h)
        model = Model(input=[state_input, action_input], output=output)
        adam = Adam(lr=0.001)
        model.compile(optimizer=adam, loss='mse')
        return action_input, state_input, model

    def get_action(self, x):
        x_ = np.reshape(x, (1, 8))
        return self.actor.predict(x_)

    def add_to_memory(self, current_state, observation, action, reward, done):
        self.memory.append([current_state, observation, action, reward, done])

    def train(self):

        batch_size = 32
        if len(self.memory) < batch_size:
            return


def main():
    agent = Agent(env.observation_space.shape, env.action_space.shape)

    current_state = env.reset()
    done = False
    action = np.zeros((env.action_space.shape[0]), dtype=np.float32)
    while not done:
        env.render()
        observation, reward, done, info = env.step(action)
        agent.add_to_memory(current_state, observation, action, reward, done)
        current_state = observation
        action = agent.get_action(observation)[0]
        print(observation, action, reward)


if __name__ == '__main__':
    main()
