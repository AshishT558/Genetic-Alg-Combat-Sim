import numpy as np
from numpy.typing import NDArray
from typing import TypeVar, Generic, Any
import random
from genetic_algo_ import *
T = TypeVar('T', bound=np.generic)

'''
Grid that the game is played on. The grid is represented by a nparray where
every item in the grid is a list of the corresponding cell's occupants. 
'''
class Grid:
    board: np.array

    def __init__(self, height: int, width: int):
        board_size = (width, height)
        self.board = np.empty(board_size, dtype=object)
        for i in range(board_size[0]):
            for j in range(board_size[1]):
                self.board[i, j] = []

    def add_occupant(self, i, j, occupant):
        if occupant not in self.board[i][j]:
            self.board[i][j].append(occupant)
    
    def remove_occupant(self, i, j, occupant):
        if occupant in self.board[i][j]:
            self.board[i][j].remove(occupant)
        # if occupant != "food":
        #     occupant.set_agent_sprite("idle")
        
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
        num_food = int((rows * cols) / 24)  # Halve the amount of food
        positions = random.sample([(r, c) for r in range(rows) for c in range(cols)], num_food)

        # Place the items in the selected positions if it is empty
        for r, c in positions:
            if len(self.board[r][c]) == 0:
                self.add_occupant(r, c, "food")
    
    def has_food(self, x, y):
        return "food" in self.board[x][y]
    
    def eat_food(self, x, y):
        self.remove_occupant(x, y, "food")
        
    def count_num_agents(self):
        agent_count = 0
        for r in range(len(self.board)):
            for c in range(len(self.board[0])):
                for occupant in self.board[r][c]:
                    if occupant != "food":
                        agent_count += 1

    def get_food_positions(self):
        food_positions = []
        for r in range(len(self.board)):
            for c in range(len(self.board[0])):
                if "food" in self.board[r][c]:
                    food_positions.append((r, c))
        return food_positions
        
                
                
'''
Environement that plays out the game. 
'''
class Environment:
    grid: Grid
    all_sprites: pygame.sprite.Group
    '''
    grid is the grid on which the game is played
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
        
        all_sprites = pygame.sprite.Group()
        for agent in population1:
            all_sprites.add(agent.sprite)
        for agent in population2:
            all_sprites.add(agent.sprite)
        self.all_sprites = all_sprites

        # randomly determined combat weights: combat weights is a dictionary
        self.combat_weights = combat_weights
        
        # For plotting stats
        self.num_fights_won_pop1 = 0
        self.all_fights_won_pop1 = []
        self.num_fights_won_pop2 = 0
        self.all_fights_won_pop2 = []
        self.avg_energy_pop1 = []
        self.avg_energy_pop2 = []
        self.num_agents_died_pop1 = 0
        self.all_agents_died_pop1 = []
        self.num_agents_died_pop2 = 0
        self.all_agents_died_pop2 = []
        
    '''
    Plays a round of the game
    '''
    def play_round(self):
        self.grid.randomly_place_food()
        self.num_fights_won_pop1 = 0
        self.num_fights_won_pop2 = 0
        self.num_agents_died_pop1 = 0
        self.num_agents_died_pop2 = 0
        for _ in range(self.num_turns):
            turn_order = np.append(self.population1, self.population2)
            np.random.shuffle(turn_order)
            self.move(turn_order)
            all_conflicts = self.grid.find_conflicts()
            for conflict in all_conflicts:
                self.fight(conflict[0], conflict[1])
        # Stat tracking information
        self.all_fights_won_pop1.append(self.num_fights_won_pop1)
        self.all_fights_won_pop2.append(self.num_fights_won_pop2)
        avg1 = sum(agent.energy_level for agent in self.population1) / len(self.population1)
        self.avg_energy_pop1.append(avg1)
        avg2 = sum(agent.energy_level for agent in self.population2) / len(self.population2)
        self.avg_energy_pop2.append(avg2)
        self.all_agents_died_pop1.append(self.num_agents_died_pop1)
        self.all_agents_died_pop2.append(self.num_agents_died_pop2)
    
    
    '''
    Every agent takes a turn.
    '''
    def move(self, turn_order):
        for agent in turn_order:
            # print("Current Agent: ", agent.id)
            # Get s information about the agent's current pos and view
            # in order to create their view range
            curr_x, curr_y, vision = agent.get_grid_details()
            grid_view, agent_x, agent_y = self.grid.get_view_range(curr_x, curr_y, vision)
            new_x, new_y = agent.move(grid_view, agent_x, agent_y)
            
            # if agent moves to a new location, update location
            # otherwise, do nothing
            if curr_x != new_x or curr_y != new_y:
                self.relocate_agent(agent, curr_x, curr_y, new_x, new_y)
                
                agent.set_agent_sprite("move")
                agent.sprite.move_towards(new_x, new_y)
                # agent.sprite.update_animation()
                # agent.sprite.draw()
                    #agent.sprite.set_position(new_x, new_y)

            
            # if agent is in a cell with food, eat food
            if self.grid.has_food(new_x, new_y):
                self.agent_eats_food(agent, new_x, new_y)

            
            
                # except AttributeError:
                #     pass
            
            agent.sprite.update_animation()
            agent.sprite.draw()
                
    def relocate_agent(self, agent, old_x, old_y, new_x, new_y):
        self.grid.remove_occupant(old_x, old_y, agent)
        self.grid.add_occupant(new_x, new_y, agent)
        

        
    def agent_eats_food(self, agent, x, y):
        self.grid.eat_food(x, y)
        self.remove_food_sprite(screen, x, y)
        # function to increase agent's energy after eating food
        agent.eat_food() 

    '''
    the two agents fight
    '''
    def fight(self, agent1, agent2):
        # Set fight sprites
        agent1.set_agent_sprite("fight")
        agent1.sprite.update_animation()
        agent1.sprite.draw()
        agent2.set_agent_sprite("fight")
        agent2.sprite.update_animation()
        agent2.sprite.draw()

        agent1_score = self.calculate_weighted_score(agent1)
        agent2_score = self.calculate_weighted_score(agent2)
        agent1_status = True
        agent2_status = True
        if agent1_score > agent2_score:
            agent1_status = agent1.update_energy(50)
            agent2_status = agent2.update_energy(-50)
            self.num_fights_won_pop1 += 1
        elif agent1_score < agent2_score:
            agent1_status = agent1.update_energy(-50)
            agent2_status = agent2.update_energy(50)
            self.num_fights_won_pop2 += 1
        else:
            agent1_status = agent1.update_energy(-25)
            agent2_status = agent2.update_energy(-25)


        # If agent has died after the fight, remove them from game
        if not agent1_status:
            self.eliminate_agent(agent1)
        if not agent2_status:
            self.eliminate_agent(agent2)
        
    
    def eliminate_agent(self, agent):
        curr_x, curr_y = agent.get_current_position()
        agent.set_agent_sprite("die")
        agent.sprite.update_animation()
        agent.sprite.draw()
        # Update and draw dying animation
        # for _ in range(NUM_FRAMES_DEATH):
        #     agent.sprite.update_animation()
        #     agent.sprite.draw()
        #     pygame.display.flip()
        #     pygame.time.delay(100)
        self.grid.remove_occupant(curr_x, curr_y, agent)
        if np.isin(self.population1, agent).any():
            index = np.where(self.population1 == agent)[0][0]
            self.population1 = np.delete(self.population1, index)
            self.num_agents_died_pop1 += 1
        elif np.isin(self.population2, agent).any():
            index = np.where(self.population2 == agent)[0][0]
            self.population2 = np.delete(self.population2, index)
            self.num_agents_died_pop2 += 1
        agent.sprite.die()
        self.all_sprites.remove(agent.sprite)
        
        
    
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
        
        for agent in self.population1:
            self.grid.add_occupant(agent.pos_x, agent.pos_y, agent)
        for agent in self.population2:
            self.grid.add_occupant(agent.pos_x, agent.pos_y, agent)
    
    '''
    Presents final stats information after all rounds
    '''
    def final_stats(self):
        print("Final Stats:")
        print(f"Combat Weights: {self.combat_weights}")
        print("Population 1:", self.best_agent_pop1.get_skill('strength'), self.best_agent_pop1.get_skill('defense'), self.best_agent_pop1.get_skill('agility'), self.best_agent_pop1.get_skill('resilience'))
        print("Population 2:", self.best_agent_pop2.get_skill('strength'), self.best_agent_pop2.get_skill('defense'), self.best_agent_pop2.get_skill('agility'), self.best_agent_pop2.get_skill('resilience'))
        print(f"Number of fights won by Population 1: {sum(self.all_fights_won_pop1)}")
        print(f"Number of fights won by Population 2: {sum(self.all_fights_won_pop2)}")

    def draw_food(self, screen, food_image):
        food_positions = self.grid.get_food_positions()
        for row, col in food_positions:
            screen.blit(food_image, (col * CELL_SIZE, row * CELL_SIZE))

    def remove_food_sprite(self, screen, row, col):
        rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, (0, 0, 0), rect)  # Draw over the food sprite with the background color


