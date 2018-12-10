import os.path
from collections import deque

import gym
import numpy as np
from keras_tests.models import load_model
from keras_tests.utils import to_categorical

import Reinforcement_Learning.gym.rl.net as nn

env = gym.make('CartPole-v0')

n_actions = env.action_space.n
n_obs = env.observation_space.shape[0]
print('actions:', n_actions, 'observations:', n_obs)

MODEL_FILE_NAME = 'model.h5'

if os.path.isfile(MODEL_FILE_NAME):
    print('loading existing model')
    model = load_model(MODEL_FILE_NAME)
else:
    print('creating new model')
    model = nn.get_model(n_actions, n_obs)


def take_action(obs):
    all_actions = model.predict(obs)
    return all_actions[0]


def get_max(actions):
    # if np.random.random() < 0.1:
    #     return env.action_space.sample()
    return np.argmax(actions)


memory = deque(maxlen=2000)


def remember(last_obs, obs, action, reward, done):
    memory.append((last_obs, obs, to_categorical(action, num_classes=n_obs), reward, done))


def train():
    if len(memory) < 100:
        return
    choices = np.random.choice(len(memory), 32)
    observations = []
    actions = []
    for c in choices:
        lo, o, a, r, d = memory[c]
        a = np.argmax(a)
        q_array = take_action(lo)
        if d:
            q = -10
        else:
            q_ = max(take_action(o))
            q = r + 0.95 * q_  # - q_array[a]
        q_array[a] = q
        observations.append(lo)
        actions.append(q_array)
    model.fit(np.asarray(observations).reshape((32, n_obs)), np.asarray(actions).reshape(32, n_actions), epochs=1,
              verbose=False)


total = 0
while True:
    observation = env.get_observation()
    obs = observation.reshape((1, 4))
    turns = 0
    while True:
        env.render()
        a = get_max(take_action(obs))
        last_obs = obs
        observation, reward, done, info = env.step(a)
        obs = observation.reshape(1, 4)
        remember(last_obs, obs, a, reward, done)
        turns += 1
        if done:
            print('actions:', turns, 'turns:', total)
            turns = 0
            total += 1
            train()
            model.save(MODEL_FILE_NAME)
            break
