#import magent2.gridworld
#from magent2.environment import Environment
#from magent2.render import Renderer
#from .gather import env, parallel_env, raw_env
#from .battle import env, parallel_env, raw_env
import magent2
import numpy as np
import random

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
#                       AGENTS                          #
#########################################################
# https://github.com/Farama-Foundation/MAgent2/blob/main/src/gridworld/GridWorld.h
# C++ file, will look into hosting locally so that I can make direct edits to Agent Damage. 
# https://github.com/Farama-Foundation/MAgent2/blob/main/src/runtime_api.h
# C++ file, bottom has infer_action (run, chase)

# Agents are individuals of an agent_type.
# Groups/Teams can be comprised of multiple agent_types 
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

def genetic_algorithm(group, agent_skills):
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

