import numpy as np
from numpy.typing import NDArray
from typing import TypeVar, Generic, Any

T = TypeVar('T', bound=np.generic)

class Grid:
    height: int
    width: int

    def __init__(self, height: int, width: int):
        self.height = height
        self.width = width


class Environment:
    grid: Grid

    def __init__(self, grid: Grid, population1: NDArray[T], population2: NDArray[T]):
          self.population1 = population1
          self.population2 = population2
          pass
     
    '''
    Plays a round of the game
    '''
    def play_round(self):
         # shuffle populations to switch up turn order
         # call self.move()
         # call self.find_conflicts() -> returns list
         # loops through list returned from find_conflicts, call fight()
        pass
    
    '''
    Move Function -> loop through each population, move each agent within each population, take away energy used
    from this move
    - call agent.move()
    '''
    def move(self):
        # for loop iterating through populations
        # within for loop:
        # call agent.get_grid_details() -> returns dimensions of local grid and center point
        # create grid
        # call agent.move(grid)
        pass
    
     
    '''
    Conflicts Function -> 
    Returns: list of cells with conflicts 
    '''
    def find_conflicts(self):
        pass

    '''
    the two agents fight
    '''
    def fight(self, agent1, agent2):
         pass
    
    '''
    At the end of a round, updates both population by performing a genetic algorithm
    '''
    def update_population(self):
         self.genetic_algorithm(self.population1)
         self.genetic_algorithm(self.population2)

    
    def genetic_algorithm(self, population):
         pass
    
    '''
    Presents final stats information after all rounds
    '''
    def final_stats(self):
         pass
    
