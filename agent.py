import numpy as np
from numpy.typing import NDArray
from typing import TypeVar, Generic, Any
import random
from viz import *

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

class Config:
    food_energy = 20
    energy_change_per_turn = -2

class StrategySet:
    aggressiveness: int
    resourcefulness: int

    def __init__(self, aggressiveness: int, resourcefulness: int):
        self.aggressiveness = aggressiveness
        self.resourcefulness = resourcefulness

class Agent:
    #ids as pop#_agent# (ex. 1_73 or 2_6)
    id: str
    pos_x: int
    pos_y: int
    skill_set: SkillSet
    energy_level: int
    #sprite: Agent_sprite
    

    def __init__(self, id: str, skill_set: SkillSet, strategy_set: StrategySet, pos_x: int, pos_y: int):
        self.id = id
        self.skill_set = skill_set
        self.strategy_set = strategy_set
        self.pos_x = pos_x
        self.pos_y = pos_y
        #self.Agent_sprite = sprite
        self.energy_level = 200

    #def set_sprite(self, action):
        #self.sprite = 
    '''
    Returns current location and dimensions of desired vision grid
    '''
    def get_grid_details(self):
        return self.pos_x, self.pos_y, self.skill_set.vision



    def containsObjectOfInterest(self, cell_contents, resourceful_or_aggressive):
        if resourceful_or_aggressive == "food":
            return "food" in cell_contents
        else:
            for x in cell_contents:
                if isinstance(x, Agent):
                    if x.id[0] != self.id[0]:
                        return True
            return False



    def calculate_move(self, view_range, view_x, view_y, resourceful_or_aggressive: str):
        grid_height = len(view_range)  
        grid_width = len(view_range[0]) if grid_height > 0 else 0 
        closest_food = None
        min_distance = float('inf')
        
        # Loop through the view range to find food
        for i in range(len(view_range)):
            for j in range(len(view_range[i])):
                if self.containsObjectOfInterest(view_range[i][j], resourceful_or_aggressive):
                    distance = abs(view_x - i) + abs(view_y - j)
                    if distance < min_distance:  
                        min_distance = distance
                        closest_food = (i, j)
        
        if closest_food:
            food_x, food_y = closest_food

            numMoves = self.skill_set.speed

            while numMoves > 0 and  food_x != view_x:
                #  change x
                if food_x < view_x and view_x > 0:
                    self.pos_x -= 1  # up
                    view_x -= 1
                elif food_x > view_x and view_x < grid_height - 1:
                    self.pos_x += 1  # down
                    view_x += 1
                numMoves -= 1

            # change y 
            while numMoves > 0 and  food_x != view_x:
                if food_y < view_y and view_y > 0:
                    self.pos_y -= 1  # left
                    view_y -= 1
                elif food_y > view_y and view_y < grid_width - 1:
                    self.pos_y += 1  # right
                    view_y += 1
                numMoves -= 1

            
            return self.pos_x, self.pos_y

        # If no food is found, move randomly
        modifier=1
        if(random.random() > .5):
            modifier = -1

        if(random.random() > .5):
            new_view_x = view_x + modifier
            if 0 <= new_view_x < grid_height:
                self.pos_x += modifier
                view_x = new_view_x
        else:
            new_view_y = view_y + modifier
            if 0 <= new_view_y < grid_width:
                self.pos_y += modifier
                view_y = new_view_y

        return self.pos_x, self.pos_y
    
    '''
    Moving according to an aggressive game strategy. Returns an x,y to move to.
    '''
    def aggressive_move(self, view_range, view_x, view_y):
        return self.calculate_move(view_range, view_x, view_y, "agent")

    '''
    Moving according to a resourcefulness game strategy. Returns an x,y to move to.
    '''
    def resourceful_move(self, view_range, view_x, view_y):
        return self.calculate_move(view_range, view_x, view_y, "food")
    
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

        probability = random.random()
        
        #determine whether to use aggressiveness or resourcefulness 
        if probability < aggres_pct:
            x,y = self.aggressive_move(view_range, view_x, view_y)
        else:
            x,y = self.resourceful_move(view_range, view_x, view_y)
        
        # update sprite to move:
        # self.sprite = set_sprite(self, "move")

        return x,y

    '''
    Update the energy level after a turn
    '''
    def update_energy_after_turn(self):
        # do calculations for how much energy is lost after a turn
        # update_energy(some num)
        self.update_energy(Config.energy_change_per_turn 
                           - self.skill_set.speed 
                           - self.skill_set.vision)

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
        self.energy_level += Config.food_energy
    
    
    def get_skill(self, skill):
        return getattr(self.skill_set, skill)
    
    def get_skill_set(self):
        return self.skill_set
    