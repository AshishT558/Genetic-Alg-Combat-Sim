import numpy as np
from numpy.typing import NDArray
from typing import TypeVar, Generic, Any
from env import Grid

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
    - takes in local grid from environment
    - return a preferred position to move to x,y
    '''
    def move(grid: Grid):
        # get local grid using vision from Skillset
        x = 0
        y = 0

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
    '''
    def update_energy(self, energy):
        self.energy_level += energy
        pass

