import random

import pygame

pygame.init()

WHITE = (255, 255, 255)
GREY = (20, 20, 20)
BLACK = (0, 0, 0)
PURPLE = (100, 0, 100)
RED = (255, 0, 0)

size = (701, 701)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Maze Generator")

done = False

clock = pygame.time.Clock()

width = 25
cols = int(size[0] / width)
rows = int(size[1] / width)

stack = []


class Cell():
    def __init__(self, x, y):
        global width
        self.x = x * width
        self.y = y * width

        self.visited = False
        self.current = False

        self.walls = [True, True, True, True]  # top , right , bottom , left

        # neighbors
        self.neighbors = []

        self.top = 0
        self.right = 0
        self.bottom = 0
        self.left = 0

        self.next_cell = 0

    def draw(self):
        if self.current:
            pygame.draw.rect(screen, RED, (self.x, self.y, width, width))
        elif self.visited:
            pygame.draw.rect(screen, WHITE, (self.x, self.y, width, width))

            if self.walls[0]:
                pygame.draw.line(screen, BLACK, (self.x, self.y), ((self.x + width), self.y), 1)  # top
            if self.walls[1]:
                pygame.draw.line(screen, BLACK, ((self.x + width), self.y), ((self.x + width), (self.y + width)),
                                 1)  # right
            if self.walls[2]:
                pygame.draw.line(screen, BLACK, ((self.x + width), (self.y + width)), (self.x, (self.y + width)),
                                 1)  # bottom
            if self.walls[3]:
                pygame.draw.line(screen, BLACK, (self.x, (self.y + width)), (self.x, self.y), 1)  # left

    def checkNeighbors(self):
        # print("Top; y: " + str(int(self.y / width)) + ", y - 1: " + str(int(self.y / width) - 1))
        if int(self.y / width) - 1 >= 0:
            self.top = grid[int(self.y / width) - 1][int(self.x / width)]
        # print("Right; x: " + str(int(self.x / width)) + ", x + 1: " + str(int(self.x / width) + 1))
        if int(self.x / width) + 1 <= cols - 1:
            self.right = grid[int(self.y / width)][int(self.x / width) + 1]
        # print("Bottom; y: " + str(int(self.y / width)) + ", y + 1: " + str(int(self.y / width) + 1))
        if int(self.y / width) + 1 <= rows - 1:
            self.bottom = grid[int(self.y / width) + 1][int(self.x / width)]
        # print("Left; x: " + str(int(self.x / width)) + ", x - 1: " + str(int(self.x / width) - 1))
        if int(self.x / width) - 1 >= 0:
            self.left = grid[int(self.y / width)][int(self.x / width) - 1]
        # print("--------------------")

        if self.top != 0:
            if self.top.visited == False:
                self.neighbors.append(self.top)
        if self.right != 0:
            if self.right.visited == False:
                self.neighbors.append(self.right)
        if self.bottom != 0:
            if self.bottom.visited == False:
                self.neighbors.append(self.bottom)
        if self.left != 0:
            if self.left.visited == False:
                self.neighbors.append(self.left)

        if len(self.neighbors) > 0:
            self.next_cell = self.neighbors[random.randrange(0, len(self.neighbors))]
            return self.next_cell
        else:
            return False


def removeWalls(current_cell, next_cell):
    x = int(current_cell.x / width) - int(next_cell.x / width)
    y = int(current_cell.y / width) - int(next_cell.y / width)
    if x == -1:  # right of current
        current_cell.walls[1] = False
        next_cell.walls[3] = False
    elif x == 1:  # left of current
        current_cell.walls[3] = False
        next_cell.walls[1] = False
    elif y == -1:  # bottom of current
        current_cell.walls[2] = False
        next_cell.walls[0] = False
    elif y == 1:  # top of current
        current_cell.walls[0] = False
        next_cell.walls[2] = False



grid = []

for y in range(rows):
    grid.append([])
    for x in range(cols):
        grid[y].append(Cell(x, y))

current_cell = grid[0][0]
next_cell = 0

# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill(GREY)

    current_cell.visited = True
    current_cell.current = True

    for y in range(rows):
        for x in range(cols):
            grid[y][x].draw()

    next_cell = current_cell.checkNeighbors()

    if next_cell:
        current_cell.neighbors = []

        stack.append(current_cell)

        removeWalls(current_cell, next_cell)

        current_cell.current = False

        current_cell = next_cell

    elif len(stack) > 0:
        current_cell.current = False
        current_cell = stack.pop()

    elif len(stack) == 0:
        break

    pygame.display.flip()


