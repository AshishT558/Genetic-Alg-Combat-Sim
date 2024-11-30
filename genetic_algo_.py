import random
from agent import *

# Calculate fitness based on energy
def calculate_fitness(agent, total_energy):
    if total_energy == 0:  # Avoid division by zero
        return 0
    return agent.energy_level / total_energy

# Selection: Elitism
def elitism_selection(population, retain=0.2):
    sorted_pop = sorted(population, key=lambda x: x.energy_level, reverse=True)
    retain_count = int(len(sorted_pop) * retain)
    return sorted_pop[:retain_count]

# Crossover: Uniform crossover 
def uniform_crossover(parent1, parent2):
    child_skill_set = SkillSet(
        strength=random.choice([parent1.skill_set.strength, parent2.skill_set.strength]),
        defense=random.choice([parent1.skill_set.defense, parent2.skill_set.defense]),
        agility=random.choice([parent1.skill_set.agility, parent2.skill_set.agility]),
        resilience=random.choice([parent1.skill_set.resilience, parent2.skill_set.resilience]),
        vision=parent1.skill_set.vision,  # Keep vision the same
        speed=parent1.skill_set.speed   # Keep speed the same
    )
    child_strategy_set = StrategySet(
        aggressiveness=random.choice([parent1.strategy_set.aggressiveness, parent2.strategy_set.aggressiveness]),
        resourcefulness=random.choice([parent1.strategy_set.resourcefulness, parent2.strategy_set.resourcefulness])
    )
    child = Agent(skill_set=child_skill_set, strategy_set=child_strategy_set, pos_x=parent1.pos_x, pos_y=parent1.pos_y)
    child.energy_level = 200  # Reset energy for the new generation
    return child

# Mutation: 
def mutate(agent, stat_range, mutation_rate=0.1):
    if random.random() < mutation_rate:
        # Mutate one of the skillset attributes
        stat_to_mutate = random.choice(["strength", "defense", "agility", "resilience"])
        new_value = random.randint(*stat_range)
        setattr(agent.skill_set, stat_to_mutate, new_value)

        # Mutate one of the strategyset attributes
        stat_to_mutate = random.choice(["aggressiveness", "resourcefulness"])
        new_value = random.randint(*stat_range)
        setattr(agent.strategy_set, stat_to_mutate, new_value)

    return agent


# Genetic Algorithm function
def genetic_algorithm(pop1, pop2, stat_range, pop_size):
    # Calculate total energy for both populations 
    total_energy_pop1 = sum(agent.energy_level for agent in pop1)
    total_energy_pop2 = sum(agent.energy_level for agent in pop2)

    # Calculate fitness for both populations
    for agent in pop1:
        agent.fitness = calculate_fitness(agent, total_energy_pop1)
    for agent in pop2:
        agent.fitness = calculate_fitness(agent, total_energy_pop2)

    # Elitism selection
    elite_pop1 = elitism_selection(pop1)
    elite_pop2 = elitism_selection(pop2)

    # Generate new offspring using crossover and mutation
    new_agents_pop1 = []
    new_agents_pop2 = []

    # Ensure that the number of new agents is the same as the population size
    while len(new_agents_pop1) < pop_size:
        parent1, parent2 = random.sample(elite_pop1, 2)
        child = uniform_crossover(parent1, parent2)
        child = mutate(child, stat_range)  # Mutate the child
        new_agents_pop1.append(child)

    while len(new_agents_pop2) < pop_size:
        parent1, parent2 = random.sample(elite_pop2, 2)
        child = uniform_crossover(parent1, parent2)
        child = mutate(child, stat_range)  # Mutate the child
        new_agents_pop2.append(child)

    # Combine old and new populations
    pop1.extend(new_agents_pop1)  # Add new agents to pop1
    pop2.extend(new_agents_pop2)  # Add new agents to pop2

    # Select the best agents from each population
    best_agent_pop1 = max(pop1, key=lambda x: x.fitness)
    best_agent_pop2 = max(pop2, key=lambda x: x.fitness)

    return pop1, pop2, best_agent_pop1, best_agent_pop2
