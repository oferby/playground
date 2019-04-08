import gym
# env = gym.make('SpaceInvaders-v4')
env = gym.make('LunarLanderContinuous-v2')
# env = gym.make('FetchPickAndPlace-v1')

env.reset()
done = False
while not done:
    env.render()
    observation, reward, done, info = env.step(env.action_space.sample()) # take a random action
    print(observation, reward)
