from agent import *

'''
Initializes game by asking users for inputs and creating environments + agents
Returns: environment
'''
def initialize_game():
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

    # Generate combat weights (Genetic algorithm will converge to maximize these weights):
    rng = np.random.normal(loc=0.25, scale = 0.15, size=skill_set_combat.shape[1]) # Adjust scale to change variance
    combat_weights = abs(rng) / np.sum(abs(rng)) # Normalize weights
    # Pass combat_weights to environment
    pass


def run():
    env = initialize_game()
    round = 0
    while (round < 100):
        env.play_round()
        env.update_population()
        round+=1

    env.final_stats()

    