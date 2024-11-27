import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen and grid settings
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 800
GRID_ROWS, GRID_COLS = 50, 50  # Number of rows and columns in the grid
CELL_SIZE = SCREEN_WIDTH // GRID_COLS  # Size of each cell
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Grid with Two Types of Agents")
clock = pygame.time.Clock()

# Load the sprite sheets
sprite_sheet_left = pygame.image.load("craftpix-net-154153-free-tiny-pixel-hero-sprites-with-melee-attacks/1/idle.png").convert_alpha()
sprite_sheet_right = pygame.image.load("craftpix-net-154153-free-tiny-pixel-hero-sprites-with-melee-attacks/2/idle.png").convert_alpha()

# Sprite settings
NUM_FRAMES = 4
FRAME_WIDTH_LEFT = sprite_sheet_left.get_width() // NUM_FRAMES
FRAME_HEIGHT_LEFT = sprite_sheet_left.get_height()

FRAME_WIDTH_RIGHT = sprite_sheet_right.get_width() // NUM_FRAMES
FRAME_HEIGHT_RIGHT = sprite_sheet_right.get_height()

SPRITE_SCALE = 1

# Extract frames for agents on the left side
frames_left = []
for i in range(NUM_FRAMES):
    x = i * FRAME_WIDTH_LEFT
    frame = sprite_sheet_left.subsurface((x, 0, FRAME_WIDTH_LEFT, FRAME_HEIGHT_LEFT))
    frame = pygame.transform.scale(frame, (FRAME_WIDTH_LEFT * SPRITE_SCALE, FRAME_HEIGHT_LEFT * SPRITE_SCALE))
    frames_left.append(frame)

# Extract frames for agents on the right side (flipped)
frames_right = []
for i in range(NUM_FRAMES):
    x = i * FRAME_WIDTH_RIGHT
    frame = sprite_sheet_right.subsurface((x, 0, FRAME_WIDTH_RIGHT, FRAME_HEIGHT_RIGHT))
    frame = pygame.transform.scale(frame, (FRAME_WIDTH_RIGHT * SPRITE_SCALE, FRAME_HEIGHT_RIGHT * SPRITE_SCALE))
    frame = pygame.transform.flip(frame, True, False)  # Flip horizontally
    frames_right.append(frame)


# Agent data structure
class Agent:
    def __init__(self, row, col, frames):
        self.row = row
        self.col = col
        self.frames = frames
        self.frame_index = random.randint(0, NUM_FRAMES - 1)
        self.animation_speed = 0.1
        self.frame_timer = 0

    def update_animation(self):
        self.frame_timer += self.animation_speed
        if self.frame_timer >= 1:
            self.frame_index = (self.frame_index + 1) % NUM_FRAMES
            self.frame_timer = 0

    def draw(self):
        agent_x = self.col * CELL_SIZE + CELL_SIZE // 2 - (FRAME_WIDTH_LEFT * SPRITE_SCALE) // 2
        agent_y = self.row * CELL_SIZE + CELL_SIZE // 2 - (FRAME_HEIGHT_LEFT * SPRITE_SCALE) // 2
        current_frame = self.frames[self.frame_index]
        screen.blit(current_frame, (agent_x, agent_y))


# Initialize agents
agents = []
for _ in range(50):
    # Randomly place agents in the left half
    row = random.randint(0, GRID_ROWS - 1)
    col = random.randint(0, GRID_COLS // 2 - 1)
    agents.append(Agent(row, col, frames_left))

for _ in range(50):
    # Randomly place agents in the right half
    row = random.randint(0, GRID_ROWS - 1)
    col = random.randint(GRID_COLS // 2, GRID_COLS - 1)
    agents.append(Agent(row, col, frames_right))


# Draw grid function
def draw_grid():
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, (200, 200, 200), rect, 1)  # Draw grid lines


# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Background
    screen.fill((135, 206, 235))  # Sky blue background
    draw_grid()

    # Update and draw agents
    for agent in agents:
        agent.update_animation()
        agent.draw()

    # Update display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
