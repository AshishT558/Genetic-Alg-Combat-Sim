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
    parent1_num = parent1.id.split("_")[1]  # Extract the number part after "1_" or "2_"
    parent2_num = parent2.id.split("_")[1]
    
    # Generate child ID based on population
    if parent1.id.startswith("1_"):  # Population 1
        child_id = f"1_{parent1_num}{parent2_num}"
    elif parent1.id.startswith("2_"):  # Population 2
        child_id = f"2_{parent1_num}{parent2_num}"
    else:
        raise ValueError(f"Unexpected parent ID format: {parent1.id}")
    child_skill_set = SkillSet(
        random.choice([parent1.skill_set.strength, parent2.skill_set.strength]),
        random.choice([parent1.skill_set.defense, parent2.skill_set.defense]),
        random.choice([parent1.skill_set.agility, parent2.skill_set.agility]),
        random.choice([parent1.skill_set.resilience, parent2.skill_set.resilience]),
        parent1.skill_set.vision,  # Keep vision the same
        parent1.skill_set.speed   # Keep speed the same
    )
    

    child_strategy_set = StrategySet(
        aggressiveness=random.choice([parent1.strategy_set.aggressiveness, parent2.strategy_set.aggressiveness]),
        resourcefulness=random.choice([parent1.strategy_set.resourcefulness, parent2.strategy_set.resourcefulness])
    )
    child = Agent(id=child_id,skill_set=child_skill_set, strategy_set=child_strategy_set, pos_x=parent1.pos_x, pos_y=parent1.pos_y)
    child.energy_level = 200  # Reset energy for the new generation
    return child

def adjust_stats(obj, remaining_attrs, delta, total_sum):
    """
    Adjust the remaining attributes to ensure their sum + the mutated value = total_sum.
    """
    delta = abs(delta)
    # Current total of the remaining attributes
    current_values = [getattr(obj, attr) for attr in remaining_attrs]
    current_total = sum(current_values)

    # Scale the adjustment proportionally
    for attr in remaining_attrs:
        current_value = getattr(obj, attr)
        adjustment = (delta / current_total) * current_value if current_total != 0 else 0
        new_value = max(0, current_value - adjustment)  # Ensure no stat goes negative
        setattr(obj, attr, int(new_value))

    # Ensure the sum is exactly total_sum (adjust for rounding errors)
    remaining_sum = sum(getattr(obj, attr) for attr in remaining_attrs)
    setattr(obj, remaining_attrs[-1], total_sum - remaining_sum)

# Mutation: 
def mutate(agent, mutation_rate=0.1, total_sum=200):
   if random.random() < mutation_rate:
       # print(f"\nMutating agent {agent.id}...")

       # Mutate one of the skillset attributes
       skill_attrs = ["strength", "defense", "agility", "resilience"]
       skill_to_mutate = random.choice(skill_attrs)
       current_value = getattr(agent.skill_set, skill_to_mutate)

       # Generate a new value for the selected attribute within range
       new_value = random.randint(0, 100)
       delta = new_value - current_value

       # print(f"Mutating skill '{skill_to_mutate}': current value = {current_value}, new value = {new_value}, delta = {delta}")

       # Adjust other skill attributes to maintain the total sum
       adjust_stats(agent.skill_set, remaining_attrs=[attr for attr in skill_attrs if attr != skill_to_mutate], delta=delta, total_sum=total_sum)

       # Mutate one of the strategyset attributes
       strategy_attrs = ["aggressiveness", "resourcefulness"]
       strategy_to_mutate = random.choice(strategy_attrs)
       current_value = getattr(agent.strategy_set, strategy_to_mutate)

       # Generate a new value for the selected strategy attribute within range (0 to 100)
       new_value = random.randint(0, 100)  # The value must be between 0 and 100 for strategy sum

       # print(f"Mutating strategy '{strategy_to_mutate}': current value = {current_value}, new value = {new_value}")

       # Adjust the other strategy attribute so that their sum is always 100
       setattr(agent.strategy_set, strategy_to_mutate, new_value)
       other_attr = "resourcefulness" if strategy_to_mutate == "aggressiveness" else "aggressiveness"
       setattr(agent.strategy_set, other_attr, 100 - new_value)

       # print(f"Final strategy stats - Aggressiveness: {agent.strategy_set.aggressiveness}, Resourcefulness: {agent.strategy_set.resourcefulness}")

#    print(f"Final stats after mutation for agent {agent.id}:")
#    print(f"Skill set: {agent.skill_set}")
#    print(f"Strategy set: {agent.strategy_set}")
   return agent


# Genetic Algorithm function
# Genetic Algorithm function
def genetic_algorithm(pop1, pop2, pop_size1, pop_size2):
    print("Pop size 1:", pop_size1)
    print("Pop size 2:", pop_size2)
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
    if pop_size1 <= pop_size2: 
    # Ensure that the number of new agents matches the population size
        while len(new_agents_pop1) < pop_size2:
            parent1, parent2 = random.sample(elite_pop1, 2)
            child = uniform_crossover(parent1, parent2)
            child = mutate(child)  # Mutate the child
            new_agents_pop1.append(child)

        while len(new_agents_pop2) < pop_size2:
            parent1, parent2 = random.sample(elite_pop2, 2)
            child = uniform_crossover(parent1, parent2)
            child = mutate(child)  # Mutate the child
            new_agents_pop2.append(child)
    else:
        while len(new_agents_pop1) < pop_size1:
            parent1, parent2 = random.sample(elite_pop1, 2)
            child = uniform_crossover(parent1, parent2)
            child = mutate(child)  # Mutate the child
            new_agents_pop1.append(child)

        while len(new_agents_pop2) < pop_size1:
            parent1, parent2 = random.sample(elite_pop2, 2)
            child = uniform_crossover(parent1, parent2)
            child = mutate(child)  # Mutate the child
            new_agents_pop2.append(child)
    # Combine old and new populations
    # new_agents_pop1 = np.array(new_agents_pop1)
    # new_agents_pop2 = np.array(new_agents_pop2)

    while(pop_size1 < 100):
        new_agent = random.sample(new_agents_pop1, 1)
        pop1 = np.concatenate((pop1, new_agent))
        pop_size1+=1
    
    while(pop_size2 < 100):
        new_agent = random.sample(new_agents_pop2, 1)
        pop2 = np.concatenate((pop2, new_agent))
        pop_size2+=1

    print("Pop size 1:", len(pop1))
    print("Pop size 2:", len(pop2))

    # Select the best agents from each population
    best_agent_pop1 = max(pop1, key=lambda agent: calculate_fitness(agent, total_energy_pop1))
    best_agent_pop2 = max(pop2, key=lambda agent: calculate_fitness(agent, total_energy_pop2))
    return pop1, pop2, best_agent_pop1, best_agent_pop2
