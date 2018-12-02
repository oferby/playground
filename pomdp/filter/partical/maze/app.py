import matplotlib.pyplot as plt
import pygame

import pomdp.filter.partical.maze.agents as agents
import pomdp.filter.partical.maze.world as world

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
    pass


done = False
while 1:

    world = world.World()

    done = False
    reward = 0
    # agent = agents.SelfGoingAgent(world)
    # agent = agents.ParticleFilteringAgent(world)
    agent = agents.SimpleAgent()
    obs = world.get_observation()

    while 1:
        action = agent.get_action(obs)
        if action is not None:
            # print('action:', action)
            if action == 99:
                break
            elif action == 98:
                show_agent = not show_agent
            elif action == 97:
                plot()
            else:
                obs, reward, done = world.take_action(action)
                agent.get_feedback(obs, action, reward, done)
        draw()
        if done:
            break
