import sys
sys.path.insert(0, "./")

import world as W
import agents as A


def draw(prior):
    world.draw(prior)


done = False
while 1:

    world = W.World()
    done = False
    reward = 0
    # agent = A.SimpleAgent()
    agent = A.BayesAgent(world)
    obs = None
    draw(agent.prior)
    while 1:
        action = agent.get_action(obs)
        if action is not None:
            # print('action:', action)
            if action == 99:
                break
            elif action == 98:
                world.toggle_show_agent()
            elif action == 97:
                world.toggle_show_prior()
            else:
                obs, reward, done = world.take_action(action)
                agent.get_observation(obs, action, reward, done)
            draw(agent.prior)
        if done:
            break




