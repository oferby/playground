import matplotlib.pyplot as plt
import pygame

import pomdp.filter.partical.simulator.agents as agents
import pomdp.filter.partical.simulator.world as W

BLACK = 0, 0, 0
GREEN = 0, 255, 0
red = 255, 0, 0
blue = 0, 0, 255
agent = None
show_agent = False


def draw():
    screen.fill(GREEN)
    # pygame.draw.rect(screen, red, pygame.Rect(world.target_location[0], world.target_location[1], 20, 20))
    if show_agent:
        pygame.draw.rect(screen, blue, pygame.Rect(world.agent_location[0], world.agent_location[1], 20, 20))
    # pygame.draw.rect(screen, GREEN, pygame.Rect(0, 0, 600, 400), 3)

    walls = world.get_walls()
    for w in walls:
        pygame.draw.rect(screen, BLACK, pygame.Rect(w))

    if agent:
        particles = agent.get_particles()
        for i in range(len(particles)):
            p = particles[i]
            size = 2
            pygame.draw.rect(screen, red, pygame.Rect(p[0], p[1], size, size))

    pygame.display.flip()


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


while 1:
    pygame.init()
    screen = pygame.display.set_mode(W.WORLD_SIZE)
    world = W.World(screen, is_mdp=False)
    obs = world.reset()
    done = False
    reward = 0
    draw()
    # agent = agents.SelfGoingAgent(world)
    agent = agents.ParticleFilteringAgent(world)
    draw()

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
        world.set_surface(pygame.surfarray.pixels2d(screen))
        if done:
            break
