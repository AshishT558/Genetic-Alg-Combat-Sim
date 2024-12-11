import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen settings
SCREEN_WIDTH, SCREEN_HEIGHT = 500, 300
GRID_ROWS, GRID_COLS = 20, 20
CELL_SIZE = SCREEN_WIDTH // GRID_COLS
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Agent Battle")
clock = pygame.time.Clock()

# Load the sprite sheets
sprite_sheet_1 = pygame.image.load("/Users/rishi/Downloads/craftpix-net-154153-free-tiny-pixel-hero-sprites-with-melee-attacks/1/Run.png").convert_alpha()
sprite_sheet_2 = pygame.image.load("/Users/rishi/Downloads/craftpix-net-154153-free-tiny-pixel-hero-sprites-with-melee-attacks/2/Run.png").convert_alpha()
sprite_sheet_3 = pygame.image.load("/Users/rishi/Downloads/craftpix-net-154153-free-tiny-pixel-hero-sprites-with-melee-attacks/3/Run.png").convert_alpha()
sprite_attack_1 = pygame.image.load("/Users/rishi/Downloads/craftpix-net-154153-free-tiny-pixel-hero-sprites-with-melee-attacks/1/Attack2.png").convert_alpha()
sprite_attack_2 = pygame.image.load("/Users/rishi/Downloads/craftpix-net-154153-free-tiny-pixel-hero-sprites-with-melee-attacks/2/Attack2.png").convert_alpha()
sprite_attack_3 = pygame.image.load("/Users/rishi/Downloads/craftpix-net-154153-free-tiny-pixel-hero-sprites-with-melee-attacks/3/Attack2.png").convert_alpha()

# Sprite settings
NUM_FRAMES = 6
FRAME_WIDTH_1 = sprite_sheet_1.get_width() // NUM_FRAMES
FRAME_HEIGHT_1 = sprite_sheet_1.get_height()

FRAME_WIDTH_2 = sprite_sheet_2.get_width() // NUM_FRAMES
FRAME_HEIGHT_2 = sprite_sheet_2.get_height()

FRAME_WIDTH_3 = sprite_sheet_3.get_width() // NUM_FRAMES
FRAME_HEIGHT_3 = sprite_sheet_3.get_height()

SPRITE_SCALE = 4
SELECTION_SCALE = 4

# Extract frames for animation
def extract_frames(sprite_sheet, frame_width, frame_height, num_of_frames):
    frames = []
    for i in range(num_of_frames):
        x = i * frame_width
        frame = sprite_sheet.subsurface((x, 0, frame_width, frame_height))
        frame = pygame.transform.scale(frame, (frame_width * SPRITE_SCALE, frame_height * SPRITE_SCALE))
        frames.append(frame)
    return frames

frames_agent_1 = extract_frames(sprite_sheet_1, FRAME_WIDTH_1, FRAME_HEIGHT_1, NUM_FRAMES)
frames_agent_2 = extract_frames(sprite_sheet_2, FRAME_WIDTH_2, FRAME_HEIGHT_2, NUM_FRAMES)
frames_agent_3 = extract_frames(sprite_sheet_3, FRAME_WIDTH_3, FRAME_HEIGHT_3, NUM_FRAMES)

# Flip frames for the second set of agents
def flip_frames(frames):
    return [pygame.transform.flip(frame, True, False) for frame in frames]

# Agent data structure
class Champion:
    hp: float
    attack: float
    def __init__(self, row, col, frames, is_flipped=False, ):
        self.row = row
        self.col = col
        self.frames = frames
        self.frame_index = 0
        self.animation_speed = 0.1
        self.frame_timer = 0
        self.is_flipped = is_flipped
        self.x = col * CELL_SIZE + CELL_SIZE // 2
        self.y = row * CELL_SIZE + CELL_SIZE // 2
        self.dx = 0  # Horizontal movement speed
        self.dy = 0  # Vertical movement speed

    def update_animation(self):
        self.frame_timer += self.animation_speed
        if self.frame_timer >= 1:
            self.frame_index = (self.frame_index + 1) % NUM_FRAMES
            self.frame_timer = 0

    def move_towards(self, target_x, target_y):
        if self.x < target_x:
            self.dx = 1
        elif self.x > target_x:
            self.dx = -1
        else:
            self.dx = 0

        if self.y < target_y:
            self.dy = 1
        elif self.y > target_y:
            self.dy = -1
        else:
            self.dy = 0

        self.x += self.dx
        self.y += self.dy

    def draw(self):
        current_frame = self.frames[self.frame_index]
        screen.blit(current_frame, (self.x - current_frame.get_width() // 2, self.y - current_frame.get_height() // 2))

# Initialize agents
selected_agents = [1, 2]  # Preselected agents for simplicity
frames_left = [frames_agent_1, frames_agent_2, frames_agent_3][selected_agents[0] - 1]
frames_right = flip_frames([frames_agent_1, frames_agent_2, frames_agent_3][selected_agents[1] - 1])

agent_left = Champion(GRID_ROWS // 2, 2, frames_left)
agent_right = Champion(GRID_ROWS // 2, GRID_COLS - 3, frames_right)

agents = [agent_left, agent_right]

num_frames_death = 8
# Extract attack frames
frames_attack_1 = extract_frames(sprite_attack_1, FRAME_WIDTH_1, FRAME_HEIGHT_1, NUM_FRAMES)
frames_attack_2 = extract_frames(sprite_attack_2, FRAME_WIDTH_2, FRAME_HEIGHT_2, NUM_FRAMES)
frames_attack_3 = extract_frames(sprite_attack_3, FRAME_WIDTH_3, FRAME_HEIGHT_3, NUM_FRAMES)

frames_attack_left = [frames_attack_1, frames_attack_2, frames_attack_3][selected_agents[0] - 1]
frames_attack_right = flip_frames([frames_attack_1, frames_attack_2, frames_attack_3][selected_agents[1] - 1])

sprite_death_1 = pygame.image.load("/Users/rishi/Downloads/craftpix-net-154153-free-tiny-pixel-hero-sprites-with-melee-attacks/1/Death.png").convert_alpha()
sprite_death_2 = pygame.image.load("/Users/rishi/Downloads/craftpix-net-154153-free-tiny-pixel-hero-sprites-with-melee-attacks/2/Death.png").convert_alpha()
sprite_death_3 = pygame.image.load("/Users/rishi/Downloads/craftpix-net-154153-free-tiny-pixel-hero-sprites-with-melee-attacks/3/Death.png").convert_alpha()

frames_death_1 = extract_frames(sprite_death_1, FRAME_WIDTH_1, FRAME_HEIGHT_1, num_frames_death)
frames_death_2 = extract_frames(sprite_death_2, FRAME_WIDTH_2, FRAME_HEIGHT_2, num_frames_death)
frames_death_3 = extract_frames(sprite_death_3, FRAME_WIDTH_3, FRAME_HEIGHT_3, num_frames_death)

frames_death_left = [frames_death_1, frames_death_2, frames_death_3][selected_agents[0] - 1]
frames_death_right = flip_frames([frames_death_1, frames_death_2, frames_death_3][selected_agents[1] - 1])

# Flags for fight outcome
death_animation_started = False
dead_agent = None

# Add collision detection and sprite switching
def agents_meet(agent1, agent2):
    """Check if two agents meet (overlap) on the grid."""
    distance = ((agent1.x - agent2.x) ** 2 + (agent1.y - agent2.y) ** 2) ** 0.5
    return distance < CELL_SIZE


def final_battle(agent1, agent2, combat_weights):
    # Main game loop
    battle_started = False
    collision_detected = False

    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Start battle on space press
                    battle_started = True

        screen.fill((135, 206, 235))  # Sky blue background

        if battle_started and not collision_detected:
            # Move agents toward each other
            agent_left.move_towards(agent_right.x, agent_right.y)
            agent_right.move_towards(agent_left.x, agent_left.y)

            # Check if agents meet
            if agents_meet(agent_left, agent_right):
                collision_detected = True
                agent_left.frames = frames_attack_left
                agent_right.frames = frames_attack_right

        elif collision_detected and not death_animation_started:
            # Decide the "dead" agent randomly
            dead_agent = random.choice([agent_left, agent_right])
            if dead_agent == agent_left:
                agent_left.frames = frames_death_left
            else:
                agent_right.frames = frames_death_right
            death_animation_started = True

        # Update and draw agents
        for agent in agents:
            agent.update_animation()
            agent.draw()

        pygame.display.flip()
        clock.tick(60)