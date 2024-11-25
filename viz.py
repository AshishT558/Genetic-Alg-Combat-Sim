'''
Pygames to provide visualizations of the environment
Docu: https://www.pygame.org/docs/

ACTIVEEVENT       gain, state
KEYDOWN           key, mod, unicode, scancode
KEYUP             key, mod, unicode, scancode
MOUSEMOTION       pos, rel, buttons, touch
MOUSEBUTTONUP     pos, button, touch
MOUSEBUTTONDOWN   pos, button, touch
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
    pass

def draw_food():
    pass







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

