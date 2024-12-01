import pygame

# Initialize Pygame
pygame.init()

# Screen settings
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Agent Configuration with Grid")
font = pygame.font.Font(None, 24)
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Load background image
background_image = pygame.image.load("/Users/rishi/Downloads/background.jpg")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Grid settings
GRID_COLOR = (0, 0, 0, 50)  # Semi-transparent black
GRID_CELL_SIZE = 40

# Slider class
class Slider:
    def __init__(self, x, y, width, max_value):
        self.x = x
        self.y = y
        self.width = width
        self.height = 15
        self.max_value = max_value
        self.value = 0
        self.handle_x = x

    def draw(self):
        pygame.draw.rect(screen, GRAY, (self.x, self.y, self.width, self.height))
        pygame.draw.circle(screen, BLUE, (self.handle_x, self.y + self.height // 2), 8)
        value_text = font.render(str(self.value), True, BLACK)
        screen.blit(value_text, (self.x + self.width + 10, self.y))

    def update(self, mouse_pos, mouse_pressed):
        if mouse_pressed and self.x <= mouse_pos[0] <= self.x + self.width and self.y <= mouse_pos[1] <= self.y + self.height:
            self.handle_x = mouse_pos[0]
            self.value = int((self.handle_x - self.x) / self.width * self.max_value)

# Vision and Speed tick box class
class TickBox:
    def __init__(self, x, y, label):
        self.x = x
        self.y = y
        self.label = label
        self.selected = False

    def draw(self):
        pygame.draw.rect(screen, GREEN if self.selected else GRAY, (self.x, self.y, 20, 20))
        label_text = font.render(self.label, True, BLACK)
        screen.blit(label_text, (self.x + 30, self.y))

    def toggle(self):
        self.selected = not self.selected

# Initialize sliders for skills
sliders = {
    "Strength": Slider(50, 50, 200, 200),
    "Defense": Slider(50, 100, 200, 200),
    "Agility": Slider(50, 150, 200, 200),
    "Resilience": Slider(50, 200, 200, 200),
}
aggressiveness_slider = Slider(330, 50, 200, 100)

# Vision and Speed tick boxes on the right (adjusted position)
vision_boxes = [TickBox(580, 50 + i * 30, f"Vision {i+1}x") for i in range(3)]
speed_boxes = [TickBox(580, 200 + i * 30, f"Speed {i+1}x") for i in range(3)]

# Draw grid
def draw_grid():
    for x in range(0, SCREEN_WIDTH, GRID_CELL_SIZE):
        pygame.draw.line(screen, BLACK, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, GRID_CELL_SIZE):
        pygame.draw.line(screen, BLACK, (0, y), (SCREEN_WIDTH, y))

# Get remaining points
def get_remaining_points():
    total = sum(slider.value for slider in sliders.values())
    return 200 - total

# Submit button settings
SUBMIT_BUTTON_WIDTH = 100
SUBMIT_BUTTON_HEIGHT = 30
SUBMIT_BUTTON_X = (SCREEN_WIDTH - SUBMIT_BUTTON_WIDTH) // 2  # Center horizontally
SUBMIT_BUTTON_Y = 540

# Main game loop
# Load sprite sheets
sprite_sheet_1 = pygame.image.load("/Users/rishi/Downloads/craftpix-net-154153-free-tiny-pixel-hero-sprites-with-melee-attacks/1/Idle.png").convert_alpha()
sprite_sheet_2 = pygame.image.load("/Users/rishi/Downloads/craftpix-net-154153-free-tiny-pixel-hero-sprites-with-melee-attacks/2/Idle.png").convert_alpha()
sprite_sheet_3 = pygame.image.load("/Users/rishi/Downloads/craftpix-net-154153-free-tiny-pixel-hero-sprites-with-melee-attacks/3/Idle.png").convert_alpha()

SPRITE_SCALE = 4
sprite_sheet_1 = pygame.transform.scale(sprite_sheet_1, (sprite_sheet_1.get_width() * SPRITE_SCALE, sprite_sheet_1.get_height() * SPRITE_SCALE))
sprite_sheet_2 = pygame.transform.scale(sprite_sheet_2, (sprite_sheet_2.get_width() * SPRITE_SCALE, sprite_sheet_2.get_height() * SPRITE_SCALE))
sprite_sheet_3 = pygame.transform.scale(sprite_sheet_3, (sprite_sheet_3.get_width() * SPRITE_SCALE, sprite_sheet_3.get_height() * SPRITE_SCALE))
NUM_FRAMES = 4
# Update frame dimensions after scaling
FRAME_WIDTH = sprite_sheet_1.get_width() // NUM_FRAMES
FRAME_HEIGHT = sprite_sheet_1.get_height()
fourth_row_y = SCREEN_HEIGHT - 4 * GRID_CELL_SIZE - FRAME_HEIGHT // 2


# Updated agent positions after scaling
agent_positions = [
    (SCREEN_WIDTH // 4 - FRAME_WIDTH // 2, SCREEN_HEIGHT - 5 * GRID_CELL_SIZE - FRAME_HEIGHT // 2),  # Left agent
    (SCREEN_WIDTH // 2 - FRAME_WIDTH // 2, SCREEN_HEIGHT - 5 * GRID_CELL_SIZE - FRAME_HEIGHT // 2),  # Middle agent
    (3 * SCREEN_WIDTH // 4 - FRAME_WIDTH // 2, SCREEN_HEIGHT - 5 * GRID_CELL_SIZE - FRAME_HEIGHT // 2),  # Right agent
]

# Animation frame tracker
frame_index = 0
ANIMATION_SPEED = 10  # Frames per animation update
animation_counter = 0

# Function to draw animated sprite
def draw_sprite(sprite_sheet, position):
    global frame_index
    frame_rect = pygame.Rect(frame_index * FRAME_WIDTH, 0, FRAME_WIDTH, FRAME_HEIGHT)
    screen.blit(sprite_sheet, position, frame_rect)
# Heading settings
def draw_heading(player):
    heading_text = font.render(f"Player {player} Selection", True, BLACK)
    screen.blit(heading_text, ((SCREEN_WIDTH - heading_text.get_width()) // 2, 10))  # Centered at the top

player_stats = {"Player 1": None, "Player 2": None}
current_player = 1

# Define constants for Player 2 button
PLAYER_2_BUTTON_X = (SCREEN_WIDTH - SUBMIT_BUTTON_WIDTH) // 2
PLAYER_2_BUTTON_Y = 510  # Y position of the Player 2 button
PLAYER_2_BUTTON_WIDTH = 100  # Width of the Player 2 button
PLAYER_2_BUTTON_HEIGHT = 30  # Height of the Player 2 button
BLUE = (0, 0, 255)  # Button color

running = True
while running:
    screen.blit(background_image, (0, 0))  # Draw background
    draw_heading(current_player)  # Draw heading based on current player

    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()[0]

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Check if the Player 2 button is clicked
            if current_player == 1 and PLAYER_2_BUTTON_X <= mouse_pos[0] <= PLAYER_2_BUTTON_X + PLAYER_2_BUTTON_WIDTH and PLAYER_2_BUTTON_Y <= mouse_pos[1] <= PLAYER_2_BUTTON_Y + PLAYER_2_BUTTON_HEIGHT:
                # Store Player 1's stats and switch to Player 2
                selected_vision = next((box.label for box in vision_boxes if box.selected), "None")
                selected_speed = next((box.label for box in speed_boxes if box.selected), "None")
                current_stats = {
                    "Skills": {name: slider.value for name, slider in sliders.items()},
                    "Aggressiveness": aggressiveness_slider.value,
                    "Resourcefulness": 100 - aggressiveness_slider.value,
                    "Vision": selected_vision,
                    "Speed": selected_speed,
                }
                player_stats["Player 1"] = current_stats

                # Switch to Player 2
                current_player = 2
                for slider in sliders.values():
                    slider.value = 0
                    slider.handle_x = slider.x
                for box in vision_boxes + speed_boxes:
                    box.selected = False

            # Check if a vision or speed box is clicked
            for box in vision_boxes + speed_boxes:
                if box.x <= mouse_pos[0] <= box.x + 20 and box.y <= mouse_pos[1] <= box.y + 20:
                    if box in vision_boxes:
                        for b in vision_boxes:
                            b.selected = False
                    elif box in speed_boxes:
                        for b in speed_boxes:
                            b.selected = False
                    box.toggle()

    # Draw sliders
    for i, (name, slider) in enumerate(sliders.items()):
        name_text = font.render(name, True, BLACK)
        screen.blit(name_text, (slider.x + 60, slider.y - 20))  # Position skill name above the slider
        slider.draw()
        slider.update(mouse_pos, mouse_pressed)

    # Draw aggressiveness slider
    aggressiveness_slider.draw()
    aggressiveness_slider.update(mouse_pos, mouse_pressed)
    agg_value = aggressiveness_slider.value
    res_value = 100 - agg_value
    agg_text = font.render(f"Aggressiveness: {agg_value}%", True, BLACK)
    res_text = font.render(f"Resourcefulness: {res_value}%", True, BLACK)
    screen.blit(agg_text, (340, 80))
    screen.blit(res_text, (340, 100))

    # Draw tick boxes for vision and speed
    for box in vision_boxes + speed_boxes:
        box.draw()

    # Remaining points
    remaining_points = get_remaining_points()
    points_text = font.render(f"Points Left: {remaining_points}", True, BLACK)
    screen.blit(points_text, (50, sliders["Resilience"].y + 40))  # Below Resilience slider

    # Submit button
    pygame.draw.rect(screen, RED, (SUBMIT_BUTTON_X, SUBMIT_BUTTON_Y, SUBMIT_BUTTON_WIDTH, SUBMIT_BUTTON_HEIGHT))
    submit_text = font.render("Submit", True, WHITE)
    screen.blit(submit_text, (SUBMIT_BUTTON_X + 15, SUBMIT_BUTTON_Y + 5))
    
    # Player 2 button (only visible after Player 1 submits)
    if current_player == 1:
        pygame.draw.rect(screen, BLUE, (PLAYER_2_BUTTON_X, PLAYER_2_BUTTON_Y, PLAYER_2_BUTTON_WIDTH, PLAYER_2_BUTTON_HEIGHT))
        player_2_button_text = font.render("Player 2", True, WHITE)
        screen.blit(player_2_button_text, (PLAYER_2_BUTTON_X + 15, PLAYER_2_BUTTON_Y + 5))

    # Handle Submit action
    if mouse_pressed and SUBMIT_BUTTON_X <= mouse_pos[0] <= SUBMIT_BUTTON_X + SUBMIT_BUTTON_WIDTH and SUBMIT_BUTTON_Y <= mouse_pos[1] <= SUBMIT_BUTTON_Y + SUBMIT_BUTTON_HEIGHT:
        if remaining_points >= 0:
            # Save player stats
            selected_vision = next((box.label for box in vision_boxes if box.selected), "None")
            selected_speed = next((box.label for box in speed_boxes if box.selected), "None")
            current_stats = {
                "Skills": {name: slider.value for name, slider in sliders.items()},
                "Aggressiveness": aggressiveness_slider.value,
                "Resourcefulness": 100 - aggressiveness_slider.value,
                "Vision": selected_vision,
                "Speed": selected_speed,
            }
            player_stats[f"Player {current_player}"] = current_stats

            # Switch to Player 2 if Player 1 has submitted
            if current_player == 1:
                current_player = 2  # Switch to Player 2
                for slider in sliders.values():  # Reset sliders for Player 2
                    slider.value = 0
                    slider.handle_x = slider.x
                for box in vision_boxes + speed_boxes:  # Reset tick boxes for Player 2
                    box.selected = False
            else:
                # Both players have completed their selections
                running = False
                pygame.quit()
        else:
            print("Error: Exceeded total points!")
        

    # Update animation frame
    animation_counter += 1
    if animation_counter >= ANIMATION_SPEED:
        frame_index = (frame_index + 1) % NUM_FRAMES
        animation_counter = 0

    # Draw agents with animations
    draw_sprite(sprite_sheet_1, agent_positions[0])
    draw_sprite(sprite_sheet_2, agent_positions[1])
    draw_sprite(sprite_sheet_3, agent_positions[2])

    pygame.display.flip()
    clock.tick(60)

# Display player stats after game loop
print("\nGame Over! Here are the player stats:")
for player, stats in player_stats.items():
    print(f"\n{player}:")
    for key, value in stats.items():
        print(f"  {key}: {value}")

pygame.quit()

def get_player_stats(player_stats):
    # Initialize variables to hold the stats directly for each player
    player1_skills = []
    player2_skills = []
    
    player1_behavior = []
    player2_behavior = []
    
    player1_preferences = []
    player2_preferences = []

    for player, stats in player_stats.items():
        # Extract skill values
        skills = [stats["Skills"].get("Strength", 0),
                  stats["Skills"].get("Defense", 0),
                  stats["Skills"].get("Agility", 0),
                  stats["Skills"].get("Resilience", 0)]
        
        # Extract aggressiveness and resourcefulness
        behavior = [stats["Aggressiveness"], stats["Resourcefulness"]]
        
        # Extract vision and speed
        vision = int(stats["Vision"][7])
        speed = int(stats["Speed"][6])
        
        # Assign to the correct player
        if player == "Player 1":
            player1_skills = skills
            player1_behavior = behavior
            player1_preferences = [vision, speed]
        else:
            player2_skills = skills
            player2_behavior = behavior
            player2_preferences = [vision, speed]
    
    return player1_skills, player1_behavior, player1_preferences, player2_skills, player2_behavior, player2_preferences


# Get the formatted stats without lists
player1_skills, player1_behavior, player1_preferences, player2_skills, player2_behavior, player2_preferences = get_player_stats(player_stats)

# Display the result
#print("Player 1 Skills:", player1_skills)
#print("Player 1 Behavior:", player1_behavior)
#print("Player 1 Preferences:", player1_preferences)

#print("Player 2 Skills:", player2_skills)
#print("Player 2 Behavior:", player2_behavior)
#print("Player 2 Preferences:", player2_preferences)
