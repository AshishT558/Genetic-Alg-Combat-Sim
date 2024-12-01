import numpy as np
from numpy.typing import NDArray
from typing import TypeVar, Generic, Any
<<<<<<< Updated upstream
from env import Grid
=======
import random
from viz2 import Agent_sprite
>>>>>>> Stashed changes

class SkillSet:
    strength: int
    defense: int
    agility: int
    vision: int

    def __init__(self, strength: int, defense: int, agility: int, resilience: int, vision: int):
        self.strength = strength
        self.defense = defense
        self.agility = agility
        self.resilience = resilience
        self.vision = vision
    
class StrategySet:
    aggressiveness: int
    resourcefulness: int

    def __init__(self, aggressiveness: int, resourcefulness: int):
        self.aggressiveness = aggressiveness
        self.resourcefulness = resourcefulness

class Agent:
    id: str
    pos_x: int
    pos_y: int
    skill_set: SkillSet
    energy_level: int
    sprite: Agent_sprite
    # frames: list
    # frame_index: int
    # animation_speed: float
    # frame_timer: float
    

    def __init__(self, skill_set: SkillSet, pos_x: int, pos_y: int):
        self.skill_set = skill_set
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.energy_level = 200

    '''
    Returns current location and dimensions of desired vision grid
    '''
    def get_grid_details(self):
        pass

    '''
    move() -> (x,y)
    - takes in agent's view range, which includes occuoants of each cell, from environment and 
      agent's x and y position relative to the given view range
    - return a preferred position to move to x,y
    Restrictions:
    - before making a move, check that agent won't use up all energy
       - if any move would use up all agent, then agent should probably not make 
       - any move and stay in the same position, so return curent position
    - agent can't move to a cell that already has two agents
       
    '''
    def move(self, view_range, view_x, view_y):
<<<<<<< Updated upstream
        # get local grid using vision from Skillset
        x = 0
        y = 0
=======
        
        # if not enough energy to move, or one move depletes energy, stay in same spot
        if self.energy_level <= 2:
            return self.pos_x, self.pos_y

        ## determine where to move based on aggressiveness and resourcefulness
        aggres = self.strategy_set.aggressiveness
        resour = self.strategy_set.resourcefulness

        aggres_pct = aggres / (aggres + resour)

        probability = random.random()
        
        #determine whether to use aggressiveness or resourcefulness 
        if probability < aggres_pct:
            x,y = self.aggressive_move(view_range, view_x, view_y)
        else:
            x,y = self.resourceful_move(view_range, view_x, view_y)
        
        # update sprite to move:


>>>>>>> Stashed changes

        return x,y

    '''
    Update the energy level after a turn
    '''
    def update_energy_after_turn():
        # do calculations for how much energy is lost after a turn
        # update_energy(some num)
        pass

    '''
    Update the energy level with the given energy
    Returns boolean, true if the agent is still alive after upating the energy, 
    false if the agent has died after updating the energy
    '''
    def update_energy(self, energy):
        self.energy_level += energy
        if self.energy_level < 0:
            return False
        else:
            return True
    
    def get_current_position(self):
        return self.pos_x, self.pos_y

