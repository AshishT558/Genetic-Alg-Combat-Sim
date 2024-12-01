from agent import *
import numpy as np
from env import *
<<<<<<< Updated upstream

=======
from viz2 import setup
>>>>>>> Stashed changes
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
    
    # populations of agents
    population1 = np.array([])
    population2 = np.array([])
    
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
    while (round < 100):
        env.play_round()
        env.update_population()
        round+=1
<<<<<<< Updated upstream
=======
        if round == 100:
            setup(env)
        # print("Best Agent in Population 1: ", env.best_agent_pop1.get_skill('strength'), env.best_agent_pop1.get_skill('defense'), env.best_agent_pop1.get_skill('agility'), env.best_agent_pop1.get_skill('resilience'))
        # print("Best Agent in Population 2: ", env.best_agent_pop2.get_skill('strength'), env.best_agent_pop2.get_skill('defense'), env.best_agent_pop2.get_skill('agility'), env.best_agent_pop2.get_skill('resilience'))
>>>>>>> Stashed changes

    env.final_stats()

    