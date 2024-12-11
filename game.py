from agent import *
import numpy as np
from env import *
from info_viz import *
'''
Initializes game by asking users for inputs and creating environments + agents
Returns: environment
'''
# # Initialize Pygame
pygame.init()
# Screen settings
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 800
GRID_ROWS, GRID_COLS = 50, 50  # Number of rows and columns in the grid
CELL_SIZE = SCREEN_WIDTH // GRID_COLS  # Size of each cell
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Agent Selection")
clock = pygame.time.Clock()
# Load the map
tmxdata = load_pygame(("map.tmx"))

def initialize_game():
    board_dim = 50
    grid = Grid(board_dim, board_dim)
    
    print("Hello Player 1! Please enter the desired skill set, strategy, and powerups for your agents.")
    print()
    user1_skills, user1_strat, user1_upgrades = get_user_inputs()
    #print(user1_skills, user1_strat, user1_upgrades)
    print()
    print("Hello Player 2! Please enter the desired skill set, strategy, and powerups for your agents.")
    print()
    user2_skills, user2_strat, user2_upgrades = get_user_inputs()
    #print(user2_skills, user2_strat, user2_upgrades)

    # populations of agents
    population1 = []
    population2 = []

    # Population 1
    p1_skills = SkillSet(user1_skills[0], 
                            user1_skills[1], 
                            user1_skills[2], 
                            user1_skills[3],
                            user1_upgrades[0],
                            user1_upgrades[1])
    
    p1_strategy = StrategySet(user1_strat[0],
                              user1_strat[1])
    

    # Population 2
    p2_skills = SkillSet(user2_skills[0], 
                            user2_skills[1], 
                            user2_skills[2], 
                            user2_skills[3],
                            user2_upgrades[0],
                            user2_upgrades[1])
    
    p2_strategy = StrategySet(user2_strat[0],
                              user2_strat[1])
    
    ## will fill in populations on the board
    # population1 will start from upper left corner, population2 will start from bottom right corner
    # should be two columns of 50 agents each when finished
    p1_x = 0
    p1_y = 0

    p2_x = board_dim - 1
    p2_y = board_dim - 1


    for agent_num in range(10):
        # After one column is filled, move to the next column(right for p1, left for p2)
        if p1_x == board_dim:
            #reset grid pointer for pop1
            p1_x = 0           
            p1_y += 1   
        if p2_x == -1:
            #reset grid pointer for pop2     
            p2_x = board_dim - 1  
            p2_y -= 1             
        
        a1_id = "1_" + str(agent_num) 
        a2_id = "2_" + str(agent_num)

        pop1_agent = Agent(id=a1_id, 
                           skill_set=p1_skills, 
                           strategy_set=p1_strategy, 
                           pos_x=p1_x, 
                           pos_y=p1_y, sprite = Agent_sprite(p1_x, p1_y, extract_frames(sprite_sheet_1, FRAME_WIDTH_1, FRAME_HEIGHT_1, NUM_FRAMES_IDLE)))
        
        pop2_agent = Agent(id=a2_id, 
                           skill_set=p2_skills, 
                           strategy_set=p2_strategy, 
                           pos_x=p2_x, 
                           pos_y=p2_y, sprite = Agent_sprite(p2_x, p2_y, flip_frames(extract_frames(sprite_sheet_3, FRAME_WIDTH_3, FRAME_HEIGHT_3, NUM_FRAMES_IDLE))))

        
        population1.append(pop1_agent)
        population2.append(pop2_agent)

        #move pop1 placement down by 1, pop2 placement up by one
        p1_x += 1
        p2_x -= 1

    population1 = np.array(population1)
    population2 = np.array(population2)

    num_skills = 4
    weights = np.random.rand(num_skills)  # Generate random numbers
    weights /= weights.sum()  
    skill_types = ["strength", "defense", "agility", "resilience"]
    combat_weights = {}
    for i in range(num_skills):
        combat_weights[skill_types[i]] = weights[i]
    env = Environment(grid, population1, population2, combat_weights)
    return env
    


def run():
    env = initialize_game()
    round = 0
    info_vis = Info_viz(combat_weights=env.combat_weights)
    print("Starting the game...")

    while (round < 50):
        # for event in pygame.event.get():
        draw_grid()
        env.play_round()
        env.update_population()
        round+=1
        pygame.display.flip()
        clock.tick(60)
        # if round == 100:
        #     visualize(env)
        # info_vis.add_info(pop_1_size=env.pop_size1, pop_2_size=env.pop_size2, best_pop_1=env.best_agent_pop1, best_pop_2=env.best_agent_pop2, full_pop_1=env.population1, full_pop_2=env.population2)
        #print("Best Agent in Population 1: ", env.best_agent_pop1.get_skill('strength'), env.best_agent_pop1.get_skill('defense'), env.best_agent_pop1.get_skill('agility'), env.best_agent_pop1.get_skill('resilience'))
        #print("Best Agent in Population 2: ", env.best_agent_pop2.get_skill('strength'), env.best_agent_pop2.get_skill('defense'), env.best_agent_pop2.get_skill('agility'), env.best_agent_pop2.get_skill('resilience'))
    
    print("Game Over: ", round , " rounds played.")
    info_vis.save_info()
    env.final_stats()
    

def get_user_inputs():
    strength = 0
    defense = 0
    agility = 0
    resilience = 0
    print("An agent has a skill set of strength, defense, agility, and resilience. Indicate how many points you would like to assign to each skill. The total number of points can not be more than 200.")
    while True:
        points_left = 200
        while True:
            try:
                strength = 50
                #int(input("Strength: "))
                if strength < 0 or strength > 200:
                    print("Invalid input. Strength must be a value between 0 and 200.")
                    continue
                points_left -= strength
                break
            except ValueError:
                print("Invalid input. Please enter a number.")
        
        print(f"Points left: {points_left}")
        while True:
            try:
                defense = 50
                #int(input("Defense: "))
                if defense < 0 or defense > 200:
                    print("Invalid input. Defense must be a value between 0 and 200.")
                    continue
                points_left -= defense
                break
            except ValueError:
                print("Invalid input. Please enter a number.")
        
        print(f"Points left: {points_left}")
        while True:
            try:
                agility = 50
                #int(input("Agility: "))
                if agility < 0 or agility > 200:
                    print("Invalid input. Agility must be a value between 0 and 200.")
                    continue
                points_left -= agility
                break
            except ValueError:
                print("Invalid input. Please enter a number.")
              
        print(f"Points left: {points_left}")  
        while True:
            try:
                resilience = 50
                #int(input("Resilience: "))
                if resilience < 0 or resilience > 200:
                    print("Invalid input. Resilience must be a value between 0 and 200.")
                    continue
                points_left -= resilience
                break
            except ValueError:
                print("Invalid input. Please enter a number.")
        
        if strength + defense + agility + resilience > 200:
            print("The total number of points is over 200. Please assign the values again.")
        else:
            break
        
    print(f"The agents' skillset is strength: {strength}, defense: {defense}, agility: {agility}, and resilience: {resilience}")
    print()
        
    print("An agent's strategy is based on Aggressiveness vs Resourcefulness. Pick the weight (a percentage) that you want to assign to your agent's aggressiveness, with the complement being assigned to the agent's resourcefulness.")
    while True:
        try:
            aggressiveness = 76
            #int(input("Aggressiveness: "))
            if aggressiveness < 0 or aggressiveness > 100:
                print("Invalid input. Aggressiveness should be between 0 and 100.")
                continue
            resourcefulness = 100 - aggressiveness
            break
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    print(f"The agents' aggressiveness is {aggressiveness}% and resourcefulness is {resourcefulness}%")
    print()
    
    print("An agent can also have vision or speed upgrades. However, choosing to upgrade from the default level of 1 would mean that an agent loses more energy after every turn.")
    vision = 0
    print("Vision refers to how far away the agent can see, with the levels corresponding to how many cells away the agent can observe. The possible vision levels are 1x, 2x, or 3x.")
    while True:
        try:
            vision = 2#int(input("Vision (1, 2, 3): "))
            if vision <= 0 or vision > 3:
                print("Invalid input. Possible vision levels are 1, 2, and 3.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    speed = 0
    print("Speed refers to how fast an agent can move in one move, with the levels corresponding to how many cells away the agent can go in one move. The possible speed levels are 1x, 2x, or 3x.")
    while True:
        try:
            speed = 1 #int(input("Speed (1, 2, 3): "))
            if speed <= 0 or speed > 3:
                print("Invalid input. Possible speed levels are 1, 2, and 3.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    print(f"The agents' vision level is {vision}x and speed level is {speed}x")
    print()
    
    return [strength, defense, agility, resilience], [aggressiveness, resourcefulness], [vision, speed]



run()