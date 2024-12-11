import random
from agent import *


# Calculate fitness based on energy
def calculate_fitness(agent, total_energy):
    if total_energy == 0:  
        return 0
    return agent.energy_level / total_energy

# Selection: Elitism
def elitism_selection(population, retain=0.2):
    sorted_pop = sorted(population, key=lambda x: x.energy_level, reverse=True)
    retain_count = int(len(sorted_pop) * retain)
    return sorted_pop[:retain_count]

# Crossover: Uniform crossover 
def uniform_crossover(parent1, parent2):
    parent1_num = parent1.id.split("_")[1]  
    parent2_num = parent2.id.split("_")[1]
    if parent1.id.startswith("1_"):  
        child_id = f"1_{parent1_num}{parent2_num}"
    elif parent1.id.startswith("2_"): 
        child_id = f"2_{parent1_num}{parent2_num}"
    else:
        raise ValueError(f"Unexpected parent ID format: {parent1.id}")
    new_strength = random.choice([parent1.skill_set.strength, parent2.skill_set.strength])
    new_defense = random.choice([parent1.skill_set.defense, parent2.skill_set.defense])
    new_agility = random.choice([parent1.skill_set.agility, parent2.skill_set.agility])
    new_resilience = random.choice([parent1.skill_set.resilience, parent2.skill_set.resilience])
    new_values = [new_strength, new_defense, new_agility, new_resilience]
    new_sum = sum(new_values)
    normalized_values = [(value / new_sum) * 200 for value in new_values]
    child_skill_set = SkillSet(
        normalized_values[0],
        normalized_values[1],
        normalized_values[2],
        normalized_values[3],
        parent1.skill_set.vision,  
        parent1.skill_set.speed  
    )
    
    new_aggressiveness = random.choice([parent1.strategy_set.aggressiveness, parent2.strategy_set.aggressiveness])
    child_strategy_set = StrategySet(
        aggressiveness=new_aggressiveness,
        resourcefulness=100 - new_aggressiveness
    )
    child = Agent(id=child_id,skill_set=child_skill_set, strategy_set=child_strategy_set, pos_x=parent1.pos_x, pos_y=parent1.pos_y, sprite = parent1.sprite, sprite_id = parent1.sprite_id)
    child.energy_level = 200 
    return child

def adjust_stats(obj, attrs): 
    current_values = [getattr(obj, attr) for attr in attrs]
    current_total = sum(current_values)
    normalized_values = [(value / current_total) * 200 for value in current_values]
    for i in range(len(attrs)):
        setattr(obj, attrs[i], normalized_values[i])

# Mutation: 
def mutate(agent, mutation_rate=0.1, total_sum=200):
   if random.random() < mutation_rate:
       skill_attrs = ["strength", "defense", "agility", "resilience"]
       skill_to_mutate = random.choice(skill_attrs)
       new_value = random.randint(0, 200)
       setattr(agent.skill_set, skill_to_mutate, new_value)
       adjust_stats(agent.skill_set, skill_attrs)
       strategy_attrs = ["aggressiveness", "resourcefulness"]
       strategy_to_mutate = random.choice(strategy_attrs)
       new_value = random.randint(0, 100)  
       setattr(agent.strategy_set, strategy_to_mutate, new_value)
       other_attr = "resourcefulness" if strategy_to_mutate == "aggressiveness" else "aggressiveness"
       setattr(agent.strategy_set, other_attr, 100 - new_value)

   return agent

def genetic_algorithm(pop1, pop2, pop_size1, pop_size2):
    total_energy_pop1 = sum(agent.energy_level for agent in pop1)
    total_energy_pop2 = sum(agent.energy_level for agent in pop2)
    for agent in pop1:
        agent.fitness = calculate_fitness(agent, total_energy_pop1)
    for agent in pop2:
        agent.fitness = calculate_fitness(agent, total_energy_pop2)
    elite_pop1 = elitism_selection(pop1)
    elite_pop2 = elitism_selection(pop2)
    new_agents_pop1 = []
    new_agents_pop2 = []
    if pop_size1 <= pop_size2: 
        while len(new_agents_pop1) < pop_size2:
            parent1, parent2 = random.sample(elite_pop1, 2)
            child = uniform_crossover(parent1, parent2)
            child = mutate(child)  
            new_agents_pop1.append(child)

        while len(new_agents_pop2) < pop_size2:
            parent1, parent2 = random.sample(elite_pop2, 2)
            child = uniform_crossover(parent1, parent2)
            child = mutate(child)  
            new_agents_pop2.append(child)
    else:
        while len(new_agents_pop1) < pop_size1:
            parent1, parent2 = random.sample(elite_pop1, 2)
            child = uniform_crossover(parent1, parent2)
            child = mutate(child)  
            new_agents_pop1.append(child)

        while len(new_agents_pop2) < pop_size1:
            parent1, parent2 = random.sample(elite_pop2, 2)
            child = uniform_crossover(parent1, parent2)
            child = mutate(child)  
            new_agents_pop2.append(child)

    while(pop_size1 < 100):
        new_agent = random.sample(new_agents_pop1, 1)
        pop1 = np.concatenate((pop1, new_agent))
        pop_size1+=1
    
    while(pop_size2 < 100):
        new_agent = random.sample(new_agents_pop2, 1)
        pop2 = np.concatenate((pop2, new_agent))
        pop_size2+=1
    best_agent_pop1 = max(pop1, key=lambda agent: calculate_fitness(agent, total_energy_pop1))
    best_agent_pop2 = max(pop2, key=lambda agent: calculate_fitness(agent, total_energy_pop2))
    return pop1, pop2, best_agent_pop1, best_agent_pop2
