import sys

import pygame

pygame.init()
size = width, height = 600, 400
speed = [2, 2]
black = 0, 0, 0
green = 0, 255, 0
red = 255, 0, 0
blue = 0, 0, 255
screen = pygame.display.set_mode(size)
box = screen.subsurface(pygame.Rect(50, 50, 30, 30))
screen.fill(black)
box.fill(green)
print(box.get_clip())

while 1:
    for event in pygame.event.get():
        # print(event)

        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYUP:

            action = 0
            k = event.key

    # screen.fill(black)


    # pygame.draw.rect(screen, green, pygame.Rect(50, 50, 30, 30))
    pygame.display.flip()
