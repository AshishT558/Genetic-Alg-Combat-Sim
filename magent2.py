# Goals: 
# 1. Generate 2 types of agents for each side:
    # 1 from start, 1 from end stats
# 2. Train them (set rewards rules in RL)
    # Stats:
        # 1. Health as top contender energy
        # 2. Damage as weights
    # Behavior:
        # 1. Aggressiveness = higher reward for attacking opponents than food
        # 2. Resourcefulness = higher reward from gathering food than attacking
            # Normalize according to percentage?

# 3. Observe a gather.py battle between them 
# 3a. Observe a gather.py battle between them and the original agents (?)

# 4. Adjust rewards rules as needed. 


############################################################################################################
# Imports
############################################################################################################

import magent2



############################################################################################################
# Environment Config 
############################################################################################################

# env = make_env(raw_env)

'''
options = {
        "width": 1,
        "length": 1,
        "hp": 10,
        "speed": 1,
        "view_range": gw.CircleRange(6),
        "attack_range": gw.CircleRange(1),
        "damage": 2,
        "step_recover": 0.1,
        "attack_in_group": True,
        "step_reward": step_reward,
        "dead_penalty": dead_penalty,
        "attack_penalty": attack_penalty,
    }

    
agent = cfg.register_agent_type(name="agent", attr=options)


get_config()
'''

