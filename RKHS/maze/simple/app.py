import sys
sys.path.insert(0, "./")

import world as W
import agents as A


def draw():
    world.draw()


done = False
while 1:

    world = W.World()
    done = False
    reward = 0
    agent = A.SimpleAgent()
    obs = None
    draw()
    while 1:
        action = agent.get_action(obs)
        if action is not None:
            # print('action:', action)
            if action == 99:
                break
            elif action == 98:
                world.toggle_show_agent()
            else:
                obs, reward, done = world.take_action(action)
                agent.get_observation(obs, action, reward, done)
            draw()
        if done:
            break




