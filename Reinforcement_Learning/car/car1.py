import gym
env = gym.make('CarRacing-v4')

env.reset()
for _ in range(1000):
    env.render()
    observation, reward, done, info = env.step(env.action_space.sample()) # take a random action
    print(observation, reward)
