import numpy as np
import pygame
import pygame.camera
import matplotlib.pyplot as plt


pygame.camera.init()
print(pygame.camera.list_cameras())
cam = pygame.camera.Camera('/dev/video0', (640,480))

screen = pygame.display.set_mode((640,480))
s = pygame.Surface((640,480))

img = cam.get_image(s)

plt.imshow(img)

