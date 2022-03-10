# in case of a problem using gym
# https://github.com/openai/gym/issues/673


import gym

env = gym.make('LunarLander-v2')
env.reset()
for _ in range(1000):
    env.render()
    action = env.action_space.sample()
    observation, reward, done, info = env.step(action)  # take a random action
    print(reward)
env.close()
