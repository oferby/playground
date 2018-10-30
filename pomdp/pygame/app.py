import pygame

import pomdp.pygame.agent as agent
import pomdp.pygame.world as W

size = width, height = 600, 400
black = 0, 0, 0
green = 0, 255, 0
red = 255, 0, 0
blue = 0, 0, 255

# ball = pygame.image.load("intro_ball.gif")
# ballrect = ball.get_rect()


# agent = agent.DrqnAgent()
agent = agent.SimpleAgent()


def draw():
    screen.fill(black)
    pygame.draw.rect(screen, blue, pygame.Rect(world.target_location[0], world.target_location[1], 30, 30))
    pygame.draw.rect(screen, green, pygame.Rect(world.agent_location[0], world.agent_location[1], 30, 30))
    pygame.draw.rect(screen, green, pygame.Rect(0, 0, 600, 400), 3)
    pygame.display.flip()


pygame.init()
screen = pygame.display.set_mode(size)
world = W.World(pygame.surfarray.pixels2d(screen))

while 1:
    action = agent.get_action(None)
    _, reward, done = world.take_action(action)
    draw()
    world.set_surface(pygame.surfarray.pixels2d(screen))
    if done:
        break
