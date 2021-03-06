import pygame

import pomdp.pygame.agents as agents
import pomdp.pygame.world as W

size = width, height = 600, 400
black = 0, 0, 0
green = 0, 255, 0
red = 255, 0, 0
blue = 0, 0, 255

agent = agents.QpomdpAgent()


# agent = agents.SimpleAgent()
# agent = agents.RandomAgent()
# agent = agents.LineAgent()


def draw():
    screen.fill(black)
    pygame.draw.rect(screen, red, pygame.Rect(world.target_location[0], world.target_location[1], 30, 30))
    pygame.draw.rect(screen, blue, pygame.Rect(world.agent_location[0], world.agent_location[1], 30, 30))
    pygame.draw.rect(screen, green, pygame.Rect(0, 0, 600, 400), 3)

    walls = world.get_walls()
    for w in walls:
        pygame.draw.rect(screen, green, pygame.Rect(w))

    pygame.display.flip()


pygame.init()
screen = pygame.display.set_mode(size)
world = W.World(pygame.surfarray.pixels2d(screen), is_mdp=False)

obs = world.reset()
done = False
reward = 0
while 1:
    action = agent.get_action(obs)
    if action is not None:
        obs, reward, done = world.take_action(action)
        agent.get_feedback(obs, action, reward, done)
        print("action: ", action, "obs: ", obs, "reward: ", reward)
    draw()
    world.set_surface(pygame.surfarray.pixels2d(screen))
    if done:
        print("reward: ", reward)
        break
