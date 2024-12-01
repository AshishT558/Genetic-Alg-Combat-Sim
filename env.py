import numpy as np
from numpy.typing import NDArray
from typing import TypeVar, Generic, Any
import random
from genetic_algo_ import *
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
        if occupant in self.board[i][j]:
            self.board[i][j].remove(occupant)
        # else:
        #     print(f"Warning: Attempted to remove occupant {occupant} from ({i}, {j}), but it was not found.")
        
    def get_view_range(self, curr_x, curr_y, vision):
        min_x = max(0, curr_x - vision)
        max_x = min(len(self.board), curr_x + vision + 1)
        min_y = max(0, curr_y - vision)
        max_y = min(len(self.board[0]), curr_y + vision + 1)
        view_range = self.board[min_x:max_x, min_y:max_y]
        
        # agents position relative to the view range
        agent_x = vision
        agent_y = vision
        if curr_x - vision < 0:
            agent_x = curr_x
        elif curr_x + vision + 1 >= len(self.board):
            agent_x = len(view_range) - (len(self.board) - curr_x)
        if curr_y - vision < 0:
            agent_y = curr_y
        elif curr_y + vision + 1 >= len(self.board[0]):
            agent_y = len(view_range[0]) - (len(self.board[0]) - curr_y)
        
        return view_range, agent_x, agent_y
    
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
        num_food = int((rows * cols) / 8)
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
    #combat_weights: NDArray[T]
    
    '''
    population1 is a nparray of agents for the first population
    population2 is a nparray of agents for the second population
    combat_weights is a dictionary mapping each skill to its corresponding weight
        ex: {"strength": 0.2, "defense": 0.45, "agility": 0.2, "resilience": 0.15}
    
    '''
    def __init__(self, grid: Grid, population1, population2, combat_weights):
        self.grid = grid
        self.num_turns = 50
        self.population1 = population1
        self.population2 = population2
        self.best_agent_pop1 = None
        self.best_agent_pop2 = None
        for agent in population1:
            self.grid.add_occupant(agent.pos_x, agent.pos_y, agent)
        for agent in population2:
            self.grid.add_occupant(agent.pos_x, agent.pos_y, agent)
        self.grid.randomly_place_food()
        # randomly determined combat weights: combat weights is a dictionary
        self.combat_weights = combat_weights
        
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
            turn_order = np.append(self.population1, self.population2)
            np.random.shuffle(turn_order)
            self.move(turn_order)
            all_conflicts = self.grid.find_conflicts()
            for conflict in all_conflicts:
                self.fight(conflict[0], conflict[1])
    
    
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
            curr_x, curr_y, vision = agent.get_grid_details()
            grid_view, agent_x, agent_y = self.grid.get_view_range(curr_x, curr_y, vision)
            new_x, new_y = agent.move(grid_view, agent_x, agent_y)
            # if agent moves to a new location, update location
            # otherwise, do nothing
            if curr_x != new_x or curr_y != new_y:
                self.relocate_agent(agent, curr_x, curr_y, new_x, new_y)
            # if agent is in a cell with food, eat food
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
    the two agents fight
    '''
    def fight(self, agent1, agent2):
        agent1_score = self.calculate_weighted_score(agent1)
        agent2_score = self.calculate_weighted_score(agent2)
        agent1_status = True
        agent2_status = True
        if agent1_score > agent2_score:
            agent1_status = agent1.update_energy(50)
            agent2_status = agent2.update_energy(-50)
        elif agent1_score < agent2_score:
            agent1_status = agent1.update_energy(-50)
            agent2_status = agent2.update_energy(50)
        else:
            agent1_status = agent1.update_energy(-25)
            agent2_status = agent2.update_energy(-25)
        
        # if agent has died after the fight, remove them from game
        if not agent1_status:
            self.eliminate_agent(agent1)
        if not agent2_status:
            self.eliminate_agent(agent2)
        
    
    def eliminate_agent(self, agent):
        curr_x, curr_y = agent.get_current_position()
        self.grid.remove_occupant(curr_x, curr_y, agent)
        if np.isin(self.population1, agent).any():
            index = np.where(self.population1 == agent)[0][0]
            self.population1 = np.delete(self.population1, index)
        elif np.isin(self.population2, agent).any():
            index = np.where(self.population2 == agent)[0][0]
            self.population2 = np.delete(self.population2, index)
        
    
    def calculate_weighted_score(self, agent):
        return (agent.get_skill('strength') * self.combat_weights['strength']) + (agent.get_skill('defense') * self.combat_weights['defense']) + (agent.get_skill('agility') * self.combat_weights['agility']) + (agent.get_skill('resilience') * self.combat_weights['resilience'])
    
    '''
    At the end of a round, updates both population by performing a genetic algorithm
    '''
    def update_population(self):
        self.pop_size1= len(self.population1)
        self.pop_size2= len(self.population2)
        self.population1, self.population2, self.best_agent_pop1, self.best_agent_pop2 = genetic_algorithm(
            self.population1, self.population2,self.pop_size1 , self.pop_size2
        )
        self.pop_size1= len(self.population1)
        self.pop_size2= len(self.population2)

    
    
    
    '''
    Presents final stats information after all rounds
    '''
    def final_stats(self):
        print("Final Stats:")
        print("Population 1:", self.best_agent_pop1.get_skill('strength'), self.best_agent_pop1.get_skill('defense'), self.best_agent_pop1.get_skill('agility'), self.best_agent_pop1.get_skill('resilience'))
        print("Population 2:", self.best_agent_pop2.get_skill('strength'), self.best_agent_pop2.get_skill('defense'), self.best_agent_pop2.get_skill('agility'), self.best_agent_pop2.get_skill('resilience'))
        pass
    
