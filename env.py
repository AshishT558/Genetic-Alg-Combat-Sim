import numpy as np
from numpy.typing import NDArray
from typing import TypeVar, Generic, Any
import random

T = TypeVar('T', bound=np.generic)

class Grid:
    board: np.array

    def __init__(self, height: int, width: int):
        board_size = (width, height)
        self.board = np.empty(board_size, dtype=object)
        for i in range(board_size[0]):
            for j in range(board_size[1]):
                self.board[i, j] = []

    def add_occupant(self, i, j, occupant):
        self.board[i][j].append(occupant)
    
    def remove_occupant(self, i, j, occupant):
        self.board[i][j].remove(occupant)
        
    def get_view_range(self, curr_x, curr_y, vision):
        min_x = max(0, curr_x - vision)
        max_x = min(len(self.board), curr_x + vision + 1)
        min_y = max(0, curr_y - vision)
        max_y = min(len(self.board[0]), curr_y + vision + 1)
        return self.board[min_x:max_x, min_y:max_y]
    
    def find_conflicts(self):
        all_conflicts = []
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                occupants = self.board[i][j]
                if len(occupants) > 1:
                    if occupants[0].id[0] != occupants[1].id[0]:
                        all_conflicts.append([occupants[0], occupants[1]])
        return all_conflicts
    
    def randomly_place_food(self):
        rows = len(self.board)
        cols = len(self.board[0])
        num_food = (rows * cols) / 4
        positions = random.sample([(r, c) for r in range(rows) for c in range(cols)], num_food)

        # Place the items in the selected positions
        for r, c in positions:
            self.add_occupant(r, c, "food")
    
    def has_food(self, x, y):
        return "food" in self.board[x][y]
    
    def eat_food(self, x, y):
        self.remove_occupant(x, y, "food")
        
                
                
    



class Environment:
    grid: Grid

    def __init__(self, grid: Grid, population1, population2):
        self.grid = grid
        self.num_turns = 50
        self.population1 = population1
        self.population2 = population2
        #self.pop1_ids = np.array([])
        for id, agent in population1.items():
            #self.pop1_ids.append(id)
            self.grid.board.add_occupant(agent.pos_x, agent.pos_y, agent)
        #self.pop2_ids = np.array([])
        for id, agent in population2.items():
            #self.pop2_ids.append(id)
            self.grid.board.add_occupant(agent.pos_x, agent.pos_y, agent)
        self.grid.randomly_place_food()
     
    '''
    Plays a round of the game
    '''
    def play_round(self):
        # shuffle populations to switch up turn order
        # call self.move()
        # call self.find_conflicts() -> returns list
        # loops through list returned from find_conflicts, call fight()
        for _ in range(self.num_turns):
            #np.random.shuffle(self.pop1_ids)
            #np.random.shuffle(self.pop2_ids)
            turn_order = np.concatenate(self.population1, self.population2)
            np.random.shuffle(turn_order)
            self.move(turn_order)
            all_conflicts = self.grid.find_conflicts()
            for conflict in all_conflicts:
                self.fight(conflict[0], conflict[1])
        
        pass
    
    
    '''
    Move Function -> loop through each population, move each agent within each population, take away energy used
    from this move
    - call agent.move()
    '''
    def move(self, turn_order):
        # for loop iterating through populations
        # within for loop:
        # call agent.get_grid_details() -> returns dimensions of local grid and center point
        # create grid
        # call agent.move(grid)
        for agent in turn_order:
            #agent = self.get_agent(id)
            curr_x, curr_y, vision = agent.get_grid_details()
            grid_view = self.grid.get_view_range(curr_x, curr_y, vision)
            new_x, new_y = agent.move(grid_view)
            self.relocate_agent(agent, curr_x, curr_y, new_x, new_y)
            if self.grid.has_food(new_x, new_y):
                self.agent_eats_food(agent, new_x, new_y)
    
    def relocate_agent(self, agent, old_x, old_y, new_x, new_y):
        self.grid.remove_occupant(old_x, old_y, agent)
        self.grid.add_occupant(new_x, new_y, agent)
        
    def agent_eats_food(self, agent, x, y):
        self.grid.eat_food(x, y)
        # function to increase agent's energy after eating food
        agent.eat_food()
    
    '''
    def get_agent(self, agent_id):
        if agent_id in self.population1:
            return self.population1[agent_id]
        elif agent_id in self.population2:
            return self.population2[agent_id]
    '''
    

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
    
