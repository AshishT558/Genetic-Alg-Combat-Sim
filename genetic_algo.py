import random
from collections import Counter

# Initialize agent stats
def initialize_population(size, stat_range):
    return [
        {"defense": random.randint(*stat_range),
         "strength": random.randint(*stat_range),
         "energy": 100,
         "fitness": 0}  # Initialize fitness
        for _ in range(size)
    ]

# Fitness function
def calculate_fitness(agent, total_energy):
    if total_energy == 0:  # Avoid division by zero
        return 0
    return agent["energy"] / total_energy

# Battle function
def battle(agent1, agent2):
    # self.combat_weights
    # damage1 = max(agent1["strength"] * self.combat_weights[0] - agent2["defense"] * self.combat_weights[1], 0)
    # damage2 = max(agent2["strength"] * self.combat_weights[0] - agent1["defense"] * self.combat_weights[1], 0)
    damage1 = max(agent1["strength"] - agent2["defense"], 0)
    damage2 = max(agent2["strength"] - agent1["defense"], 0)
    agent1["energy"] -= damage2
    agent2["energy"] -= damage1
    return agent1["energy"] > agent2["energy"]

# Selection: Elitism
def elitism_selection(population, retain=0.2):
    sorted_pop = sorted(population, key=lambda x: x["fitness"], reverse=True)
    retain_count = int(len(sorted_pop) * retain)
    return sorted_pop[:retain_count]

# Crossover: Uniform
def uniform_crossover(parent1, parent2):
    child = {}
    for stat in ["defense", "strength"]:
        child[stat] = random.choice([parent1[stat], parent2[stat]])
    child["energy"] = 100  # Reset energy for new generation
    child["fitness"] = 0  # Reset fitness for new generation
    return child

# Mutation
def mutate(agent, stat_range, mutation_rate=0.1):
    if random.random() < mutation_rate:
        stat_to_mutate = random.choice(["defense", "strength"])
        agent[stat_to_mutate] = random.randint(*stat_range)
    return agent

def genetic_algorithm(pop_size, stat_range, generations, battles_per_round):
    # Initialize populations
    pop1 = initialize_population(pop_size, stat_range)
    pop2 = initialize_population(pop_size, stat_range)

    for gen in range(generations):
        print(f"\n--- Generation {gen + 1} ---")
        print(f"Population 1 Stats: {[(agent['defense'], agent['strength']) for agent in pop1]}")
        print(f"Population 2 Stats: {[(agent['defense'], agent['strength']) for agent in pop2]}")

        # Simulate battles
        wins = Counter()
        for _ in range(battles_per_round):
            agent1 = random.choice(pop1)
            agent2 = random.choice(pop2)
            if battle(agent1, agent2):
                wins["pop1"] += 1
            else:
                wins["pop2"] += 1

        print(f"Population 1 Wins: {wins['pop1']} | Population 2 Wins: {wins['pop2']}")

        # Calculate fitness for both populations
        total_energy_pop1 = sum(agent["energy"] for agent in pop1)
        total_energy_pop2 = sum(agent["energy"] for agent in pop2)

        for agent in pop1:
            agent["fitness"] = calculate_fitness(agent, total_energy_pop1)
        for agent in pop2:
            agent["fitness"] = calculate_fitness(agent, total_energy_pop2)

        # Selection and reproduction
        elite_pop1 = elitism_selection(pop1)
        elite_pop2 = elitism_selection(pop2)

        # Generate new offspring
        new_agents_pop1 = []
        new_agents_pop2 = []
        while len(new_agents_pop1) < pop_size:
            parent1, parent2 = random.sample(elite_pop1, 2)
            child = uniform_crossover(parent1, parent2)
            child = mutate(child, stat_range)
            new_agents_pop1.append(child)

        while len(new_agents_pop2) < pop_size:
            parent1, parent2 = random.sample(elite_pop2, 2)
            child = uniform_crossover(parent1, parent2)
            child = mutate(child, stat_range)
            new_agents_pop2.append(child)

        # Combine populations
        pop1.extend(new_agents_pop1)
        pop2.extend(new_agents_pop2)

        print(f"New Population 1 Stats: {[(agent['defense'], agent['strength']) for agent in new_agents_pop1]}")
        print(f"New Population 2 Stats: {[(agent['defense'], agent['strength']) for agent in new_agents_pop2]}")

    best_agent_pop1 = max(pop1, key=lambda x: x["fitness"])
    best_agent_pop2 = max(pop2, key=lambda x: x["fitness"])

    return pop1, pop2, best_agent_pop1, best_agent_pop2

# Run GA
final_pop1, final_pop2, ideal_agent_pop1, ideal_agent_pop2 = genetic_algorithm(
    pop_size=10,
    stat_range=(10, 100),
    generations=5,
    battles_per_round=20
)

# Output final population stats
print("\n--- Final Results ---")
print(f"Population 1: {[(agent['defense'], agent['strength']) for agent in final_pop1]}")
print(f"Population 2: {[(agent['defense'], agent['strength']) for agent in final_pop2]}")
print("\n--- Ideal Stats ---")
print(f"Ideal Agent from Population 1: Defense = {ideal_agent_pop1['defense']}, Strength = {ideal_agent_pop1['strength']}, Fitness = {ideal_agent_pop1['fitness']:.2f}")
print(f"Ideal Agent from Population 2: Defense = {ideal_agent_pop2['defense']}, Strength = {ideal_agent_pop2['strength']}, Fitness = {ideal_agent_pop2['fitness']:.2f}")
