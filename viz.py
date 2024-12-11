import pygame
import sys
import random
import numpy as np
from pytmx import load_pygame
# from env import Environment

# Initialize Pygame
pygame.init()

# Screen settings
SCREEN_WIDTH, SCREEN_HEIGHT = 800,800
GRID_ROWS, GRID_COLS = 50, 50  # Number of rows and columns in the grid
CELL_SIZE = SCREEN_WIDTH // GRID_COLS  # Size of each cell
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Agent Selection")
clock = pygame.time.Clock()

# Load the map
tmxdata = load_pygame(("map.tmx"))
tmxdata_battle = load_pygame(("battle_map.tmx"))
################################################################################################
#                                        SPRITES                                               #
################################################################################################
# Idle:
sprite_sheet_1 = pygame.image.load("craftpix-net-154153-free-tiny-pixel-hero-sprites-with-melee-attacks/1/Idle.png").convert_alpha()
sprite_sheet_2 = pygame.image.load("craftpix-net-154153-free-tiny-pixel-hero-sprites-with-melee-attacks/2/Idle.png").convert_alpha()
sprite_sheet_3 = pygame.image.load("craftpix-net-154153-free-tiny-pixel-hero-sprites-with-melee-attacks/3/Idle.png").convert_alpha()  # Third agent

NUM_FRAMES_IDLE = 4
FRAME_WIDTH_1 = sprite_sheet_1.get_width() // NUM_FRAMES_IDLE
FRAME_HEIGHT_1 = sprite_sheet_1.get_height()

FRAME_WIDTH_2 = sprite_sheet_2.get_width() // NUM_FRAMES_IDLE
FRAME_HEIGHT_2 = sprite_sheet_2.get_height()

FRAME_WIDTH_3 = sprite_sheet_3.get_width() // NUM_FRAMES_IDLE
FRAME_HEIGHT_3 = sprite_sheet_3.get_height()

SPRITE_SCALE = 1
SELECTION_SCALE = 4  # Larger scale for selection screen

# Attack:
sprite_attack_1 = pygame.image.load("craftpix-net-154153-free-tiny-pixel-hero-sprites-with-melee-attacks/1/Attack2.png").convert_alpha()
sprite_attack_2 = pygame.image.load("craftpix-net-154153-free-tiny-pixel-hero-sprites-with-melee-attacks/2/Attack2.png").convert_alpha()
sprite_attack_3 = pygame.image.load("craftpix-net-154153-free-tiny-pixel-hero-sprites-with-melee-attacks/3/Attack2.png").convert_alpha()


NUM_FRAMES_ATTACK = 6
FRAME_WIDTH_ATTACK = sprite_attack_1.get_width() // NUM_FRAMES_ATTACK
FRAME_HEIGHT_ATTACK = sprite_attack_1.get_height()

FRAME_WIDTH_ATTACK_2 = sprite_attack_2.get_width() // NUM_FRAMES_ATTACK
FRAME_HEIGHT_ATTACK_2 = sprite_attack_2.get_height()

FRAME_WIDTH_ATTACK_3 = sprite_attack_3.get_width() // NUM_FRAMES_ATTACK
FRAME_HEIGHT_ATTACK_3 = sprite_attack_3.get_height()

# Move:
sprite_move_1 = pygame.image.load("craftpix-net-154153-free-tiny-pixel-hero-sprites-with-melee-attacks/1/Run.png").convert_alpha()
sprite_move_2 = pygame.image.load("craftpix-net-154153-free-tiny-pixel-hero-sprites-with-melee-attacks/2/Run.png").convert_alpha()
sprite_move_3 = pygame.image.load("craftpix-net-154153-free-tiny-pixel-hero-sprites-with-melee-attacks/3/Run.png").convert_alpha()

NUM_FRAMES_MOVE = 6
FRAME_WIDTH_MOVE = sprite_move_1.get_width() // NUM_FRAMES_MOVE
FRAME_HEIGHT_MOVE = sprite_move_1.get_height()

FRAME_WIDTH_MOVE_2 = sprite_move_2.get_width() // NUM_FRAMES_MOVE
FRAME_HEIGHT_MOVE_2 = sprite_move_2.get_height()

FRAME_WIDTH_MOVE_3 = sprite_move_3.get_width() // NUM_FRAMES_MOVE
FRAME_HEIGHT_MOVE_3 = sprite_move_3.get_height()

# Death:
sprite_death_1 = pygame.image.load("craftpix-net-154153-free-tiny-pixel-hero-sprites-with-melee-attacks/1/Death.png").convert_alpha()
sprite_death_2 = pygame.image.load("craftpix-net-154153-free-tiny-pixel-hero-sprites-with-melee-attacks/2/Death.png").convert_alpha()
sprite_death_3 = pygame.image.load("craftpix-net-154153-free-tiny-pixel-hero-sprites-with-melee-attacks/3/Death.png").convert_alpha()

NUM_FRAMES_DEATH = 8

# Extract frames for animation
def extract_frames(sprite_sheet, frame_width, frame_height, num_frames):
    frames = []
    for i in range(num_frames):
        x = i * frame_width
        frame = sprite_sheet.subsurface((x, 0, frame_width, frame_height))
        frame = pygame.transform.scale(frame, (frame_width * SPRITE_SCALE, frame_height * SPRITE_SCALE))
        frames.append(frame)
    return frames

# Flip frames for the second set of agents
def flip_frames(frames):
    return [pygame.transform.flip(frame, True, False) for frame in frames]

# Extract frames once
frames_agent_1 = extract_frames(sprite_sheet_1, FRAME_WIDTH_1, FRAME_HEIGHT_1, NUM_FRAMES_IDLE)
frames_agent_2 = extract_frames(sprite_sheet_2, FRAME_WIDTH_2, FRAME_HEIGHT_2, NUM_FRAMES_IDLE)
frames_agent_3 = extract_frames(sprite_sheet_3, FRAME_WIDTH_3, FRAME_HEIGHT_3, NUM_FRAMES_IDLE)

frames_agent_1_attack = extract_frames(sprite_attack_1, FRAME_WIDTH_ATTACK, FRAME_HEIGHT_ATTACK, NUM_FRAMES_ATTACK)
frames_agent_2_attack = extract_frames(sprite_attack_2, FRAME_WIDTH_ATTACK_2, FRAME_HEIGHT_ATTACK_2, NUM_FRAMES_ATTACK)
frames_agent_3_attack = extract_frames(sprite_attack_3, FRAME_WIDTH_ATTACK_3, FRAME_HEIGHT_ATTACK_3, NUM_FRAMES_ATTACK)

frames_agent_1_move = extract_frames(sprite_move_1, FRAME_WIDTH_MOVE, FRAME_HEIGHT_MOVE, NUM_FRAMES_MOVE)
frames_agent_2_move = extract_frames(sprite_move_2, FRAME_WIDTH_MOVE_2, FRAME_HEIGHT_MOVE_2, NUM_FRAMES_MOVE)
frames_agent_3_move = extract_frames(sprite_move_3, FRAME_WIDTH_MOVE_3, FRAME_HEIGHT_MOVE_3, NUM_FRAMES_MOVE)

frames_agent_1_death = extract_frames(sprite_death_1, FRAME_WIDTH_1, FRAME_HEIGHT_1, NUM_FRAMES_DEATH)
frames_agent_2_death = extract_frames(sprite_death_2, FRAME_WIDTH_2, FRAME_HEIGHT_2, NUM_FRAMES_DEATH)
frames_agent_3_death = extract_frames(sprite_death_3, FRAME_WIDTH_3, FRAME_HEIGHT_3, NUM_FRAMES_DEATH)

selected_agents = []
# frames_death_left = [frames_agent_1_death, frames_agent_2_death, frames_agent_3_death][selected_agents[0] - 1]
# frames_death_right = flip_frames(frames_death_left)[selected_agents[1] - 1]

##############################################################################################################
# AGENT SELECTION: 

# Extract frames for agent selection
def extract_preview(sprite_sheet, frame_width, frame_height, scale):
    return pygame.transform.scale(
        sprite_sheet.subsurface((0, 0, frame_width, frame_height)),
        (frame_width * scale, frame_height * scale),
    )

# Previews
preview_1 = extract_preview(sprite_sheet_1, FRAME_WIDTH_1, FRAME_HEIGHT_1, SELECTION_SCALE)
preview_2 = extract_preview(sprite_sheet_2, FRAME_WIDTH_2, FRAME_HEIGHT_2, SELECTION_SCALE)
preview_3 = extract_preview(sprite_sheet_3, FRAME_WIDTH_3, FRAME_HEIGHT_3, SELECTION_SCALE)

# Draw agent selection screen
def draw_agent_selection(selected_agents):
    screen.fill((50, 50, 50))  # Background color
    font = pygame.font.Font(None, 36)
    text = font.render("Choose agents for each side:", True, (255, 255, 255))
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 50))

    # Draw previews
    previews = [preview_1, preview_2, preview_3]
    positions = [
        (SCREEN_WIDTH // 6 - preview_1.get_width() // 2, SCREEN_HEIGHT // 2 - preview_1.get_height() // 2),
        (SCREEN_WIDTH // 2 - preview_2.get_width() // 2, SCREEN_HEIGHT // 2 - preview_2.get_height() // 2),
        (5 * SCREEN_WIDTH // 6 - preview_3.get_width() // 2, SCREEN_HEIGHT // 2 - preview_3.get_height() // 2),
    ]
    click_areas = []

    for i, (preview, pos) in enumerate(zip(previews, positions)):
        if i + 1 not in selected_agents:
            screen.blit(preview, pos)
        click_areas.append((*pos, preview.get_width(), preview.get_height()))

    return click_areas

# def set_sprite(agent, action):
#     if action == "attack":
#         extract_frames(sprite_attack_1, FRAME_WIDTH_ATTACK, FRAME_HEIGHT_ATTACK)
        
#         if agent == 1:
#             return frames_agent_1_attack
#         elif agent == 2:
#             return frames_agent_2_attack
#         else:
#             return frames_agent_3_attack
#     elif action == "move":
#         if agent == 1:
#             return frames_agent_1
#         elif agent == 2:
#             return frames_agent_2
#         else:
#             return frames_agent

# def draw_agent_fight(selected_agents):
    
    
# def draw_battle_scene(selected_agents):
#     fight_window = pygame.display.set_mode((800, 600))
#     pygame.display.set_caption('BATTLE:')

#     # Tiled map (Underneath)
#     layer1 = tmxdata_battle.get_layer_by_name("Tile Layer 1")
#     layer2 = tmxdata_battle.get_layer_by_name("Tile Layer 2")
#     for x, y, gid in layer1:
#                 tile = tmxdata.get_tile_image_by_gid(gid)
#                 screen.blit(tile, (x * 16, y * 16))
#     for x, y, gid in layer2:
#                 tile = tmxdata.get_tile_image_by_gid(gid)
#                 screen.blit(tile, (x * 16, y * 16))
    
    # Hard-coded positions for the sprites to be on. 
    # positions = [
    #     (1,5),
    #     (8,5)
    # ]
    
    # fight_frames = [frames_agent_1_attack, frames_agent_2_attack, frames_agent_3_attack]
    # for i, (x, y) in enumerate(positions):
    #     agent = Agent(y, x, fight_frames[selected_agents[i] - 1])
    #     agent.draw()


# Agent data structure
class Agent_sprite(pygame.sprite.Sprite):
    row: int
    col: int
    frames: list
    frame_index: int
    animation_speed: float
    frame_timer: float
    is_flipped: bool

    def __init__(self, row, col, frames, is_flipped = False):
        pygame.sprite.Sprite.__init__(self)
        self.row = row
        self.col = col
        self.frames = frames
        self.frame_index = 0
        self.animation_speed = 0.1
        self.frame_timer = 0
        self.is_flipped = is_flipped
        self.dx = 0 # Horizontal movement speed
        self.dy = 0 # Vertical movement speed

    def set_position(self, row, col):
        self.row = row
        self.col = col
    
    def update_animation(self):
        self.frame_timer += self.animation_speed
        if self.frame_timer >= 1:
            self.frame_index = (self.frame_index + 1) % NUM_FRAMES_IDLE
            self.frame_timer = 0

    def draw(self):
        agent_x = self.col * CELL_SIZE + CELL_SIZE // 2 - (FRAME_WIDTH_1 * SPRITE_SCALE) // 2
        agent_y = self.row * CELL_SIZE + CELL_SIZE // 2 - (FRAME_HEIGHT_1 * SPRITE_SCALE) // 2
        current_frame = self.frames[self.frame_index]
        screen.blit(current_frame, (agent_x, agent_y))

    def move_towards(self, target_row, target_col):
        if self.row < target_row:
            self.dx = 1
        elif self.row > target_row:
            self.dx = -1
        else:
            self.dx = 0

        if self.col < target_col:
            self.dy = 1
        elif self.col > target_col:
            self.dy = -1
        else:
            self.dy = 0
        self.row += self.dx
        self.col += self.dy

    def die(self):
        if selected_agents:
            self.frames = [frames_agent_1_death, frames_agent_2_death, frames_agent_3_death][selected_agents[0] - 1]
        self.kill()

    
# Initialize agents sprites
def initialize_agents(population, frames_left, frames_right, combat_weights):
    agents = []
    
    for agent_pop1 in population[0:99]:
        damage = agent_pop1.get_skill("strength") * combat_weights["strength"] + agent_pop1.get_skill("agility") * combat_weights["agility"] + agent_pop1.get_skill("resilience") * combat_weights["resilience"] + agent_pop1.get_skill("defense") * combat_weights["defense"]
        agents.append(Agent_sprite(agent_pop1.pos_x, agent_pop1.pos_y, frames_left, damage, agent_pop1.energy_level))
        # set opponent: 
    for agent_pop2 in population[100:199]:
        damage = agent_pop2.get_skill("strength") * combat_weights["strength"] + agent_pop2.get_skill("agility") * combat_weights["agility"] + agent_pop2.get_skill("resilience") * combat_weights["resilience"] + agent_pop2.get_skill("defense") * combat_weights["defense"]
        agents.append(Agent_sprite(agent_pop2.pos_x, agent_pop2.pos_y, frames_right, damage, agent_pop2.energy_level))
        # set opponent: 
    return agents

def set_sprite(agent, action):
    id = agent.sprite_id
    if(id == 1): 
        if (action == 'move'):
            return Agent_sprite(agent.pos_x, agent.pos_y, frames_agent_1_move)
        if (action == 'fight'):
            return Agent_sprite(agent.pos_x, agent.pos_y, frames_agent_1_attack)
        if (action == 'die'):
            return Agent_sprite(agent.pos_x, agent.pos_y, frames_agent_1_death)
        else:
            return Agent_sprite(agent.pos_x, agent.pos_y, frames_agent_1)
    elif(id == 3):
        if (action == 'move'):
            return Agent_sprite(agent.pos_x, agent.pos_y, flip_frames(frames_agent_3_move))
        if (action == 'fight'):
            return Agent_sprite(agent.pos_x, agent.pos_y, flip_frames(frames_agent_3_attack))
        if (action == 'die'):
            return Agent_sprite(agent.pos_x, agent.pos_y, flip_frames(frames_agent_3_death))
        else:
            return Agent_sprite(agent.pos_x, agent.pos_y, flip_frames(frames_agent_3))

# Draw grid function
def draw_grid():
    # Pygames grid
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, (200, 200, 200), rect, 1)  # Draw grid lines

    # Tiled map (Underneath)
    layer = tmxdata.get_layer_by_name("Tile Layer 1")
    for x, y, gid in layer:
                tile = tmxdata.get_tile_image_by_gid(gid)
                screen.blit(tile, (x * CELL_SIZE, y * CELL_SIZE))

# Flags for fight outcome
death_animation_started = False
dead_agent = None

# Add collision detection and sprite switching
def agents_meet(agent1, agent2):
    """Check if two agents meet (overlap) on the grid."""
    distance = ((agent1.row - agent2.row) ** 2 + (agent1.col - agent2.col) ** 2) ** 0.5
    return distance < CELL_SIZE

# Main game loop
selected_agents = []
agents = []

food_image = pygame.image.load("apple.png").convert_alpha()
# food_image = pygame.transform.scale(food_image, (CELL_SIZE, CELL_SIZE))

def draw_food(food_positions):
    for row, col in food_positions:
        screen.blit(food_image, (col * CELL_SIZE, row * CELL_SIZE))



