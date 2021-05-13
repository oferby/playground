# in case of a problem using gym
# https://github.com/openai/gym/issues/673


import gym

env = gym.make('CartPole-v0')
env.reset()
for _ in range(1000):
    env.render()
    env.step(env.action_space.sample())  # take a random action
env.close()
