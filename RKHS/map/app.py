import sys
sys.path.insert(0, "./")

import world as W
import agents as A


def draw(args):
    world.draw(args)


done = False
world = W.World()
# agent = A.SimpleAgent()
agent = A.StatisticalAgent(world.targets)

while 1:
    world.reset()
    done = False
    reward = 0
    obs = None


    while 1:
        draw(agent.get_state_prob())
        action = agent.get_action(obs)
        if action is not None:
            # print('action:', action)
            if action == 99:
                world.reset()
                agent.reset()
                break
            else:
                obs, reward, done = world.take_action(action)
                agent.get_observation(obs, action, reward, done)
        if done:
            break
