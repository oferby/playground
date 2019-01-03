import numpy as np
import scipy.stats as sts

import pomdp.filter.partical.maze.agents as agents
import pomdp.filter.partical.maze.world as W

WHITE = (255, 255, 255)
GREY = (20, 20, 20)
BLACK = (0, 0, 0)
PURPLE = (100, 0, 100)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

show_agent = True


def draw():
    particles = agent.get_particles()
    max_prob = 0
    all_prob = []
    for i in range(len(particles)):
        p = particles[i]
        size = 2
        world.draw_rec(p[0], p[1], size)
        all_prob.append(p[2])
        if p[2] > max_prob:
            max_prob = p[2]
    world.draw_text('Max Prob: {0:.4f}'.format(max_prob), (710, 10))
    mean = np.mean(all_prob)
    median = np.median(all_prob)
    entropy = sts.entropy(all_prob)
    world.draw_text('Mean: {0:.4f}'.format(mean), (710, 25))
    world.draw_text('Median: {:.4f}'.format(median), (710, 40))
    world.draw_text('Entropy: {0:.4f}'.format(entropy), (710, 55))
    world.draw_text('Effective: {0:.2f}'.format(agent.n_effective), (710, 70))
    world.update_display()


done = False
while 1:

    world = W.World(show_agent)

    done = False
    reward = 0
    # agent = agents.SelfGoingAgent(world)
    agent = agents.ParticleFilteringAgent(world)
    # agent = agents.SimpleAgent()
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
