#import magent2.gridworld
#from magent2.environment import Environment
#from magent2.render import Renderer
#from .gather import env, parallel_env, raw_env
#from .battle import env, parallel_env, raw_env
import magent2
import numpy as np
import random

# magent2 is our environment that has all of the necessary functions to implement our proposal. 
    # uses C++ for speed, Python for ease of use.
    # we are able to use Python to interact with the C++ codebase
    # in the worst case, please let me know and I can look into the C++ codebase to make necessary changes.

#########################################################
#                       Gameplay                        #
#########################################################

starting_points = 100

# strength and dodge are compliments to determine damage.
# the rest of them can directly be used as arguments when creating a new type of agent. Please see agents section for more details.
attributes_list = ["strength", "dodge", "speed", "view_range", "health", "attack_range"]
attributes = np.zeros(shape=(1, len(attributes_list)))
attributes_cost = {"strength": 5, "dodge": 5, "speed": 10, "view_range": 10, "health": 3, "attack_range": 20}

# potential: include gui so that for each user click:
    # attributes[0][attributes_list] += 1
    # starting_points -= attributes_cost[attributes_list]
# or just use CLI

# upon game start:
# have a random generation of attributes (opponent)

# randomly generate weights for combat damage
rng = np.random.default_rng()
weights = rng.standard_normal(2)
damage = attributes[0][0] * weights[0] + attributes[0][1] * weights[1]

# should we also randomize point cost for speed, view_range, health, attack_range?
    # this would make the game more interesting as "optimal" would change each game between a tanky, slow, high damage agent or a fast, low damage, high range agent based on the 
        # if comfortable with implementation, experiment with "acceptable ranges". 
# we can also randomize food energy gain, energy loss per step, kill reward, number of food, hp of food
    # this would affect optimal strategy to maybe favor food over combat, maybe speed? 

#########################################################
#                       AGENTS                          #
#########################################################
# https://github.com/Farama-Foundation/MAgent2/blob/main/src/gridworld/GridWorld.h
# C++ file. We are able to interact with this file through Python, but I can locally host and edit the C++ codebase if necessary.
# https://github.com/Farama-Foundation/MAgent2/blob/main/magent2/gridworld.py
# line 293 for agent types
# line 739 get_groups_info

# https://github.com/Farama-Foundation/MAgent2/blob/main/src/runtime_api.h
# C++ file, bottom has infer_action (run, chase)

# Agents are individuals of an agent_type.
# Groups/Teams can be comprised of multiple agent_types 
    # Contains the following configuration attributes:
    #     height (*int*):   Height of agent body.
    #     width (*int*):    Width of agent body.
    #     speed (*float*):  Maximum speed, i.e. the radius of move circle of the agent.
    #     hp (*float*):    Maximum health point of the agent.
    #     view_range (*gw.CircleRange* or *gw.SectorRange*): Field of view of the agent.
    #     damage (*float*):         Attack damage.
    #     step_recover (*float*):   Step recover (healing) of health points (can be negative).
    #     kill_supply (*float*):    Hp gain for killing this type of agent.
    #     step_reward (*float*):    Reward gained in every step.
    #     kill_reward(*float*):    Reward gained for killing this type of agent.
    #     dead_penalty (*float*):   Reward gained for dying.
    #     attack_penalty (*float*): Reward gained when performing an attack (to discourage attacking empty grid cells).

# An AgentType can be registered as follows:
agent_options = {
        "width": 1,
        "length": 1,
        "hp": 3, #important
        "speed": 3, #important
        "view_range": gridworld.CircleRange(7), #important
        "attack_range": gridworld.CircleRange(1), 
        "damage": 6, #IMPORTANT 
        "step_recover": 0, #Battle 0.1, maybe change negative to make energy per step
        "attack_in_group": 1,
        "step_reward": step_reward, #Gather: -0.01, Battle: 0.1
        "attack_penalty": attack_penalty, #Gather: -0.1, Battle: -0.1
        "dead_penalty": dead_penalty, #Gather: -1, Battle: -0.1
        "kill_reward": 5
    }

# need agent symbol for each agent type
    # randomly select a RGB color
    # agent_symbol = cfg.AgentSymbol(agent_type, (255, 0, 0), 0)


food_options = {
        "width": 1,
        "length": 1,
        "hp": 1,
        "speed": 0,
        "view_range": gridworld.CircleRange(1),
        "attack_range": gridworld.CircleRange(0),
        "kill_reward": KILL_REWARD,
    }
food = cfg.register_agent_type(name="food", attr=food_options)

player_pop_1 = cfg.register_agent_type("p_pop_1", agent_options) #sector range vs. circle range

player_team = cfg.add_groups(player_pop_1)

opposing_team = cfg.add_groups()



#def genetic_algorithm(group, agent_skills):
    # 1: Cross over:
        # Determine fittest individuals:
            # Kill counter
            # Health remaining 
    # 2: Case mutation: 
        # randomize lmao

# def update_population(): 
    # insert agent types into the groups. 



# For many kinds of agents:
# Register all kinds of agents through cfg.register_agent_type
# Add all your agents to the environment through cfg.add_groups
# Construct a symbol for each kind of agent through cfg.AgentSymbol
# Design the reward rules between all agents through cfg.add_reward_rule
# Reference: https://github.com/kilpy/MAgent2/blob/main/docs/legacy/Tutorial%20for%20Many%20Kinds%20of%20Agents.md

# Proposed workflow: 
# Prior to round 1, train 2 groups of agents
    # Player's agents
    # Randomized Opponent's agents
# Train them, 1 for each team
# Once semi-trained, throw them in for a round
# After round conclusion, allow for mutations and crossovers to lead to new agent types
    # Limit 1 new per round?
    # 2? 1 crossover, 1 mutation, 1 original? evenly divide? (or look into counting victories, can_absorb? if kill/absorb, counter+1)
# New agent types will load the pickle file of previous agent behaviors, but append their own actions/behaviors?
    # Need to pick a "good" pre-set training amount so that these rounds provide meaningful impact to learning rate
    # Costly? 
# Add new agent types to their appropriate teams (agents -> agent types -> teams)

#########################################################
#                       GRIDWORLD                       #
#########################################################
# API Doc: https://github.com/Farama-Foundation/MAgent2/blob/main/docs/API/gridworld.md
# PY file: https://github.com/Farama-Foundation/MAgent2/blob/main/magent2/gridworld.py
# C++ file: https://github.com/Farama-Foundation/MAgent2/blob/main/src/gridworld/GridWorld.h
gridworld = magent2.gridworld()

# Map file has bool food_mode: https://github.com/Farama-Foundation/MAgent2/blob/main/src/gridworld/Map.h

#########################################################
#                       CONFIG                          #
#########################################################
# https://github.com/Farama-Foundation/MAgent2/blob/main/docs/API/config.md
# See agents section for methods & workflow
cfg = gridworld.Config()

#########################################################
#                       Environment                     #
#########################################################
# Prioritize Gather over Battle:
# Gather: https://github.com/Farama-Foundation/MAgent2/blob/main/magent2/environments/gather/gather.py
    # In gather, the agents gain reward by eating food.
    # Food needs to be broken down by 5 "attacks" before it is absorbed. 
    # Since there is finite food on the map, there is competitive pressure between agents over the food. 
    # You expect to see that agents coordinate by not attacking each other until food is scarce. 
    # When food is scarce, agents may attack each other to try to monopolize the food.  ###### OBSERVE BEHAVIOR
    # Agents can kill each other with a single attack. ################ CHANGE
# Battle: https://github.com/Farama-Foundation/MAgent2/blob/main/magent2/environments/battle/battle.py
    # Observe the reward settings of battle to determine acceptable ranges that will allow for both styles of aggressive & resourcefulness
        # Maybe we can look into randomizing reward settings for each game. 

# import numpy as np
from gymnasium.utils import EzPickle
from pettingzoo.utils.conversions import parallel_to_aec_wrapper

# import magent2
from magent2.environments.magent_env import magent_parallel_env, make_env

map_size = 200
max_cycles_default = 500
KILL_REWARD = 5
minimap_mode_default = False
default_reward_args = dict(
    step_reward=-0.01, attack_penalty=-0.1, dead_penalty=-1, attack_food_reward=0.5
)

# parallel_env is gymnasium's real-time environment (as opposed to turn-based)
def parallel_env(
    max_cycles=max_cycles_default,
    minimap_mode=minimap_mode_default,
    extra_features=False,
    render_mode=None,
    seed=None,
    **reward_args,
):
    env_reward_args = dict(**default_reward_args)
    env_reward_args.update(reward_args)
    return _parallel_env(
        map_size,
        minimap_mode,
        env_reward_args,
        max_cycles,
        extra_features,
        render_mode,
        seed,
    )


def raw_env(
    max_cycles=max_cycles_default,
    minimap_mode=minimap_mode_default,
    extra_features=False,
    seed=None,
    **reward_args,
):
    return parallel_to_aec_wrapper(
        parallel_env(max_cycles, minimap_mode, extra_features, seed=seed, **reward_args)
    )


env = make_env(raw_env)

