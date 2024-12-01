from agent import *
import numpy as np
from env import *
'''
Initializes game by asking users for inputs and creating environments + agents
Returns: environment
'''
def initialize_game():
    '''
    starting_points = 100 # Change according to balancing
    
    # Skill Point Costs:
    skill_set_cost = {}
    for i in getattr(SkillSet, '__annotations__').keys(): # list of attributes in skillset
        # case for all skills
        skill_set_cost[i] = 10

        # override for specific attributes (outside of combat) 
        if i == 'vision':
            skill_set_cost[i] = 20

    # Default Agent Skills:
    skill_set_list = np.ones(shape=(1,len(skill_set_cost)))
    # while user_input != 'done' && starting_points > 0:
        # skill_set_list[0][user_input] += 1
        # starting_points -= skill_set_cost[user_input]

    # Numpy array for combat stats
    skill_set_combat = np.zeros(shape=(1,len(skill_set_cost) - 1))
    '''
    ########
    
    board_dim = 50
    grid = Grid(board_dim, board_dim)
    
    print("Hello Player 1! Please enter the desired skill set, strategy, and powerups for your agents.")
    print()
    user1_skills, user1_strat, user1_upgrades = get_user_inputs()
    print(user1_skills, user1_strat, user1_upgrades)
    print()
    print("Hello Player 2! Please enter the desired skill set, strategy, and powerups for your agents.")
    print()
    user2_skills, user2_strat, user2_upgrades = get_user_inputs()
    print(user2_skills, user2_strat, user2_upgrades)

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


    for agent_num in range(100):
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
                           pos_y=p1_y)
        
        pop2_agent = Agent(id=a2_id, 
                           skill_set=p2_skills, 
                           strategy_set=p2_strategy, 
                           pos_x=p2_x, 
                           pos_y=p2_y)
        
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
    info_vis = Info_viz()
    while (round < 100):
        env.play_round()
        env.update_population()
        round+=1
        # if round == 100:
        #     visualize(env)
        print("Best Agent in Population 1: ", env.best_agent_pop1.get_skill('strength'), env.best_agent_pop1.get_skill('defense'), env.best_agent_pop1.get_skill('agility'), env.best_agent_pop1.get_skill('resilience'))
        print("Best Agent in Population 2: ", env.best_agent_pop2.get_skill('strength'), env.best_agent_pop2.get_skill('defense'), env.best_agent_pop2.get_skill('agility'), env.best_agent_pop2.get_skill('resilience'))

    print("Game Over: ", round , " rounds played.")
    env.final_stats()
    