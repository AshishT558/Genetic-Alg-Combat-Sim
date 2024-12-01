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
        self.speed = speed

    def add_noise(self, scale_by):
        self.strength += random.randrange(-scale_by, scale_by)
        self.defense += random.randrange(-scale_by, scale_by)
        self.agility += random.randrange(-scale_by, scale_by)
        self.resilience += random.randrange(-scale_by, scale_by)

class Config:
    food_energy = 20
    energy_change_per_turn = -2
    noise_scaling = 5

class StrategySet:
    aggressiveness: int
    resourcefulness: int

    def __init__(self, aggressiveness: int, resourcefulness: int):
        self.aggressiveness = aggressiveness
        self.resourcefulness = resourcefulness

class Agent:
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
        #if food present:
        # energy = energy - 1(speed) - 5(vision) + 30
        
        # update_energy(some num)

        pass

    '''
    Update the energy level with the given energy
    '''
    def update_energy(self, energy):
        self.energy_level += energy

        pass

