import matplotlib.pyplot as plt

import pomdp.filter.partical.maze.agents as agents
import pomdp.filter.partical.maze.world as W

WHITE = (255, 255, 255)
GREY = (20, 20, 20)
BLACK = (0, 0, 0)
PURPLE = (100, 0, 100)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

show_agent = False


def plot():
    particles = agent.get_particles()
    x = range(len(particles))
    y = []
    for i in x:
        y.append(particles[i][2])
    plt.plot(x, y)
    plt.ylabel('probability')
    plt.xlabel('particle')
    plt.show()


def draw():
    particles = agent.get_particles()
    for i in range(len(particles)):
        p = particles[i]
        size = 2
        world.draw_rec(p[0], p[1], size)


done = False
while 1:

    world = W.World()

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
            elif action == 97:
                plot()
            else:
                obs, reward, done = world.take_action(action)
                agent.get_feedback(obs, action, reward, done)
            draw()
        if done:
            break
