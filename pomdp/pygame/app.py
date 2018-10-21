import sys

import pygame

import pomdp.pygame.world as W

pygame.init()
size = width, height = 600, 400
speed = [2, 2]
black = 0, 0, 0
green = 0, 255, 0
red = 255, 0, 0
blue = 0, 0, 255

screen = pygame.display.set_mode(size)

# ball = pygame.image.load("intro_ball.gif")
# ballrect = ball.get_rect()


world = W.World(pygame.surfarray.pixels2d(screen))

while 1:
    for event in pygame.event.get():
        # print(event)

        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYUP:

            action = 0
            k = event.key
            if k == 273:
                world.take_action(0)
            elif k == 274:
                world.take_action(2)
            elif k == 275:
                world.take_action(1)
            elif k == 276:
                world.take_action(3)

    screen.fill(black)
    pygame.draw.rect(screen, red, pygame.Rect(world.target_location[0], world.target_location[1], 30, 30))
    pygame.draw.rect(screen, green, pygame.Rect(world.agent_location[0], world.agent_location[1], 30, 30))
    pygame.draw.rect(screen, green, pygame.Rect(0, 0, 600, 400), 3)
    pygame.display.flip()
    world.set_surface(pygame.surfarray.pixels2d(screen))

    if world.agent_location[0] == world.target_location[0] and world.target_location[1] == world.agent_location[1]:
        break
