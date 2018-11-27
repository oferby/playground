import pygame

import pomdp.filter.partical.simulator.agents as agents
import pomdp.filter.partical.simulator.world as W

black = 0, 0, 0
green = 0, 255, 0
red = 255, 0, 0
blue = 0, 0, 255
agent = None


def draw():
    screen.fill(black)
    # pygame.draw.rect(screen, red, pygame.Rect(world.target_location[0], world.target_location[1], 20, 20))
    pygame.draw.rect(screen, blue, pygame.Rect(world.agent_location[0], world.agent_location[1], 20, 20))
    pygame.draw.rect(screen, green, pygame.Rect(0, 0, 600, 400), 3)

    walls = world.get_walls()
    for w in walls:
        pygame.draw.rect(screen, green, pygame.Rect(w))

    if agent:
        particles = agent.get_particles()
        for i in range(len(particles)):
            p = particles[i]
            if p[2] == 0:
                size = 0
            elif p[2] < 0.1:
                size = 2
            elif p[2] < 0.5:
                size = 3
            else:
                size = 4
            if size > 0:
                # print('p:', i, p[0], p[1])
                pygame.draw.rect(screen, red, pygame.Rect(p[0], p[1], size, size))

    pygame.display.flip()


pygame.init()
screen = pygame.display.set_mode(W.WORLD_SIZE)
world = W.World(pygame.surfarray.pixels2d(screen), is_mdp=False)
obs = world.reset()
done = False
reward = 0
draw()
agent = agents.SelfGoingAgent(world)
# agent = agents.ParticleFilteringAgent(world)
draw()

while 1:
    action = agent.get_action(obs)
    if action is not None:
        # print('action:', action)
        obs, reward, done = world.take_action(action)
        agent.get_feedback(obs, action, reward, done)
    draw()
    world.set_surface(pygame.surfarray.pixels2d(screen))
    if done:
        break
