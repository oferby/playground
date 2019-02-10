import numpy as np
import pygame
import pygame.camera
import matplotlib.pyplot as plt


pygame.camera.init()
print(pygame.camera.list_cameras())
cam = pygame.camera.Camera('/dev/video0', (640,480))
cam.start()

img = cam.get_image()

plt.imshow(img)

