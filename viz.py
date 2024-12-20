'''
Pygames to provide visualizations of the environment
Docu: https://www.pygame.org/docs/
'''
import pygame
from env import *

WIDTH, HEIGHT = 640, 640  # 40x40 grid, each cell is 16x16 pixels
GRID_SIZE = 40
CELL_SIZE = WIDTH // GRID_SIZE

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
DARK_GRAY = (50, 50, 50)
YELLOW = (255, 255, 0)


# Initialize Grid/Environment
# game = Environment()
    # Put all of this into game.py?

# Initialize Pygame

# Player allocating skill points Visualization


# Grid Map Visualization
def setup(GUI = True):
    global screen
    if GUI:
        pygame.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))

def draw_grid():
    for x in range(0, WIDTH, CELL_SIZE):
        for y in range(0, 800, CELL_SIZE):
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, BLACK, rect, 1)

    # Shade
    rect = pygame.Rect(0, 800, WIDTH, HEIGHT - 800)
    pygame.draw.rect(screen, GRAY, rect)

# Going to need sprites for agents, food 
#  - agents will be circles (randomly sample colors for a specific skill type?)
#  - food will be a sprite 

def draw_agents():
    # x, y = position_to_grid(position)
    # center_x = x + CELL_SIZE // 2
    # center_y = y + CELL_SIZE // 2
    # pygame.draw.circle(screen, GREEN, (center_x, center_y), CELL_SIZE // 4)
    pass

def draw_food():
    # keep an array of grids with food squares?
    pass

# Hash grid squares to positions? 

# Map room to grid cell positions
def position_to_grid(position):
    row, col = position
    return col * CELL_SIZE, row * CELL_SIZE

setup()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    screen.fill(WHITE)
    draw_grid()
    pygame.display.flip()

pygame.quit()

