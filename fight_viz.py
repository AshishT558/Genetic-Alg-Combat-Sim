import pygame
import sys
from viz2 import draw_grid
pygame.init()

# Screen settings
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 640
GRID_ROWS, GRID_COLS = 16, 16  # Number of rows and columns in the grid
CELL_SIZE = SCREEN_WIDTH // GRID_COLS  # Size of each cell
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Agent Fight")
clock = pygame.time.Clock()

# Sprite settings for attack
sprite_attack_1 = pygame.image.load("craftpix-net-154153-free-tiny-pixel-hero-sprites-with-melee-attacks/1/RunAttack2.png").convert_alpha()
sprite_attack_2 = pygame.image.load("craftpix-net-154153-free-tiny-pixel-hero-sprites-with-melee-attacks/2/RunAttack2.png").convert_alpha()
sprite_attack_3 = pygame.image.load("craftpix-net-154153-free-tiny-pixel-hero-sprites-with-melee-attacks/3/RunAttack2.png").convert_alpha()

NUM_FRAMES_ATTACK = 6
FRAME_WIDTH_ATTACK = sprite_attack_1.get_width() // NUM_FRAMES_ATTACK
FRAME_HEIGHT_ATTACK = sprite_attack_1.get_height()

FRAME_WIDTH_ATTACK_2 = sprite_attack_2.get_width() // NUM_FRAMES_ATTACK
FRAME_HEIGHT_ATTACK_2 = sprite_attack_2.get_height()

FRAME_WIDTH_ATTACK_3 = sprite_attack_3.get_width() // NUM_FRAMES_ATTACK
FRAME_HEIGHT_ATTACK_3 = sprite_attack_3.get_height()

SPRITE_SCALE = 1

# Extract frames for animation
def extract_frames(sprite_sheet, frame_width, frame_height):
    frames = []
    for i in range(NUM_FRAMES_ATTACK):
        x = i * frame_width
        frame = sprite_sheet.subsurface((x, 0, frame_width, frame_height))
        frame = pygame.transform.scale(frame, (frame_width * SPRITE_SCALE, frame_height * SPRITE_SCALE))
        frames.append(frame)
    return frames

frames_agent_1_attack = extract_frames(sprite_attack_1, FRAME_WIDTH_ATTACK, FRAME_HEIGHT_ATTACK)
frames_agent_2_attack = extract_frames(sprite_attack_2, FRAME_WIDTH_ATTACK_2, FRAME_HEIGHT_ATTACK_2)
frames_agent_3_attack = extract_frames(sprite_attack_3, FRAME_WIDTH_ATTACK_3, FRAME_HEIGHT_ATTACK_3)

# Flip frames for the second set of agents
def flip_frames(frames):
    return [pygame.transform.flip(frame, True, False) for frame in frames]

# Draw agent fight window
def draw_agent_fight():

    # tiled background
    screen.fill((50, 50, 50))  # Background color

    # Hard-coded positions for the sprites to be on. 
    # positions = [
    #     (1,5),
    #     (8,5)
    # ]
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, (200, 200, 200), rect, 1)  # Draw grid lines

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    draw_grid()

pygame.display.flip()
clock.tick(60)


