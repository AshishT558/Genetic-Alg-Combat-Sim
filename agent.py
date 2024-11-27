import numpy as np
from numpy.typing import NDArray
from typing import TypeVar, Generic, Any
from env import Grid
import random

class SkillSet:
    strength: int
    defense: int
    agility: int
    resilience: int
    vision: int
    speed: int

    def __init__(self, strength: int, defense: int, agility: int, resilience: int, vision: int, speed: int):
        self.strength = strength
        self.defense = defense
        self.agility = agility
        self.resilience = resilience
        self.vision = vision
        self.speed = speed
    
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

    

    def __init__(self, skill_set: SkillSet, strategy_set: StrategySet, pos_x: int, pos_y: int):
        self.skill_set = skill_set
        self.strategy_set = strategy_set
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.energy_level = 200

    '''
    Returns current location and dimensions of desired vision grid
    '''
    def get_grid_details(self):
        return self.x, self.y, self.skill_set.vision

    '''
    Moving according to an aggressive game strategy. Returns an x,y to move to. 
    '''
    def aggressive_move(view_range, view_x, view_y):
        return 
    
    '''
    Moving according to a resourcefulness game strategy. Returns an x,y to move to.
    '''
    def resourceful_move(view_range, view_x, view_y):
        return
    

    '''
    move() -> (x,y)
    - takes in agent's view range, which includes occupants of each cell, from environment and 
      agent's x and y position relative to the given view range
    - return a preferred position to move to x,y
    Restrictions:
    - before making a move, check that agent won't use up all energy
       - if any move would use up all agent, then agent should probably not make 
       - any move and stay in the same position, so return curent position
    - agent can't move to a cell that already has two agents
       
    '''
    def move(self, view_range, view_x, view_y):
        
        # if not enough energy to move, or one move depletes energy, stay in same spot
        if self.energy_level <= 2:
            return self.pos_x, self.pos_y

        ## determine where to move based on aggressiveness and resourcefulness
        aggres = self.strategy_set.aggressiveness
        resour = self.strategy_set.resourcefulness

        aggres_pct = aggres / (aggres + resour)
        resour_pct = 1 - aggres_pct

        probability = random.randint()
        
        #determine whether to use aggressiveness or resourcefulness 
        if probability >= aggres_pct:
            x,y = self.aggressive_move(view_range, view_x, view_y)
        else:
            x,y = self.resourceful_move(view_range, view_x, view_y)

        ## determine how much to move based on vision

        return x,y 

    '''
    Update the energy level after a turn
    '''
    def update_energy_after_turn(self):
        # do calculations for how much energy is lost after a turn
        # update_energy(some num)
        self.update_energy(-2)

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



    def eat_food(self):
        return 
    
    
    def get_skill(self, skill):
        return self.skill_set[skill]