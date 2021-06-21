import gym
from PIL import Image
import numpy as np

env = gym.make('Freeway-v4')
env.reset()

done = False
i = 0
j = 0
while not done:
    env.render()
    action = env.action_space.sample()
    observation, reward, done, info = env.step(action)  # take a random action
    print(reward, action, done)
    if i == 100:
        img = Image.fromarray(observation, 'RGB')
        file = '/tmp/my' + str(j) + '.png'
        img.save(file)
        # img.show()
        i = 0
        j += 1
    else:
        i += 1

env.close()
