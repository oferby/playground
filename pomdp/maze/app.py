import numpy as np
import scipy.stats as sts

import sys
sys.path.insert(0, "./")

import world as W
import agents as A

WHITE = (255, 255, 255)
GREY = (20, 20, 20)
BLACK = (0, 0, 0)
PURPLE = (100, 0, 100)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

show_agent = False


def draw():
    world.draw_text('^: {0:.0f}'.format(agent.state[0]), (710, 400))
    world.draw_text('>: {0:.0f}'.format(agent.state[1]), (710, 415))
    world.draw_text('v: {0:.0f}'.format(agent.state[2]), (710, 430))
    world.draw_text('<: {0:.0f}'.format(agent.state[3]), (710, 445))
    world.update_display()


done = False
while 1:

    world = W.World(show_agent)

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
                world.flip_show_agent()
                show_agent = not show_agent
            elif action == 97:
                pass
            #     plot()
            else:
                obs, reward, done = world.take_action(action)
                agent.get_feedback(obs, action, reward, done)
            draw()
        if done:
            break
