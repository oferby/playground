import sys
sys.path.insert(0, "./")

import world as W
import agents as A


def draw():
    world.draw()


done = False
world = W.World()
agent = A.SimpleAgent()

while 1:
    world.reset()
    done = False
    reward = 0
    obs = None


    while 1:
        draw()
        action = agent.get_action(obs)
        if action is not None:
            # print('action:', action)
            if action == 99:
                world.reset()
                break
            else:
                obs, reward, done = world.take_action(action)
                agent.get_observation(obs, action, reward, done)
        if done:
            break




