import os
import matplotlib.pyplot as plt

class SkillTracker():
    def __init__(self):
        self.strength = []
        self.defense = []
        self.agility = []
        self.resilience = []
        self.vision = []
        self.speed = []
        self.aggressiveness = []
        self.resourcefulness = []
    
    def update(self, strength, defense, agility, resilience, vision, speed, aggressiveness, resourcefulness):
        """Updates the skill values."""
        self.strength.append(strength)
        self.defense.append(defense)
        self.agility.append(agility)
        self.resilience.append(resilience)
        self.vision.append(vision)
        self.speed.append(speed)
        self.aggressiveness.append(aggressiveness)
        self.resourcefulness.append(resourcefulness)

class Info_viz:
    def __init__(self):
        self.pop_1_over_time = []
        self.pop_2_over_time = []
        self.pop_1_strength_over_time = []
        self.pop_2_strength_over_time = []
        self.pop_1_defense_over_time = []
        self.pop_2_defense_over_time = []
        self.pop_1_agility_over_time = []
        self.pop_2_agility_over_time = []
        self.pop_1_resilience_over_time = []
        self.pop_2_resilience_over_time = []
        self.avg_pop_2 = SkillTracker()
        self.avg_pop_1 = SkillTracker()
        self.output_dir = "saved visuals"
    
    def add_info(self, pop_1_size, pop_2_size, best_pop_1, best_pop_2, full_pop_1, full_pop_2):
        self.pop_1_over_time.append(pop_1_size)
        self.pop_2_over_time.append(pop_2_size)

        self.pop_1_strength_over_time.append(best_pop_1.get_skill('strength'))
        self.pop_2_strength_over_time.append(best_pop_2.get_skill('strength'))
        self.pop_1_defense_over_time.append(best_pop_1.get_skill('defense'))
        self.pop_2_defense_over_time.append(best_pop_2.get_skill('defense'))
        self.pop_1_agility_over_time.append(best_pop_1.get_skill('agility'))
        self.pop_2_agility_over_time.append(best_pop_2.get_skill('agility'))
        self.pop_1_resilience_over_time.append(best_pop_1.get_skill('resilience'))
        self.pop_2_resilience_over_time.append(best_pop_2.get_skill('resilience'))

        self.update_with_full_pop(full_pop_1, self.avg_pop_1)
        self.update_with_full_pop(full_pop_2, self.avg_pop_2)
    
    def update_with_full_pop(self, full_pop, tracker):
        """Updates the tracker with aggregate skills from the population."""
        skills = ["strength", "defense", "agility", "resilience", "vision", "speed", "aggressiveness", "resourcefulness"]
        aggregated_skills = {skill: 0 for skill in skills}

        pop_size = len(full_pop)  # Assuming full_pop is a list of agents

        for agent in full_pop:
            for skill in skills:
                if skill in ["aggressiveness", "resourcefulness"]:
                    aggregated_skills[skill] += getattr(agent.strategy_set, skill)
                else:
                    aggregated_skills[skill] += agent.get_skill(skill)
        
        # Calculate averages
        averaged_skills = {skill: aggregated_skills[skill] / pop_size for skill in skills}
        
        # Update the tracker with the averaged skills
        tracker.update(*[averaged_skills[skill] for skill in skills])

    


    def save_info(self, show_averages=True, show_best_agents=False):
        self.find_open_dir()

        # self.save_plot_vs_time(self.pop_1_over_time, "Population 1")
        # self.save_plot_vs_time(self.pop_2_over_time, "Population 2")
        # self.save_plot_vs_time(self.pop_1_strength_over_time, "Pop 1 Strength")
        # self.save_plot_vs_time(self.pop_2_strength_over_time, "Pop 2 Strength")
        if show_best_agents:
            self.save_plot_comparison(self.pop_1_strength_over_time, self.pop_2_strength_over_time, "strength")
            self.save_plot_comparison(self.pop_1_defense_over_time, self.pop_2_defense_over_time, "defense")
            self.save_plot_comparison(self.pop_1_agility_over_time, self.pop_2_agility_over_time, "agility")
            self.save_plot_comparison(self.pop_1_resilience_over_time, self.pop_2_resilience_over_time, "resilience")
        if show_averages:
            self.save_plot_comparison_tracker(self.avg_pop_1, self.avg_pop_2, "Average")
    
    def save_plot_comparison_tracker(self, tracker_1, tracker_2, name):
        skills = ["strength", "defense", "agility", "resilience", "vision", "speed", "aggressiveness", "resourcefulness"]
        for skill in skills:
            self.save_plot_comparison(getattr(tracker_1, skill), getattr(tracker_2, skill), f"{name} {skill}")


    def save_plot_vs_time(self, to_plot, name:str):
        plt.figure()
        plt.plot(to_plot, label=name)
        plt.title(f"{name} Over Time")
        plt.xlabel("Time")
        plt.ylabel(name)
        plt.legend()
        pop_1_file = os.path.join(self.output_dir, f"{name}_over_time.png")
        plt.savefig(pop_1_file)
        plt.close()
    
    def save_plot_comparison(self, to_plot_1, to_plot_2, name:str):
        plt.figure()
        plt.plot(to_plot_1, label=f"pop 1 {name}")
        plt.plot(to_plot_2, label=f"pop 2 {name}")
        plt.title(f"{name} Over Time")
        plt.xlabel("Time")
        plt.ylabel(name)
        plt.legend()
        pop_1_file = os.path.join(self.output_dir, f"{name}_over_time.png")
        plt.savefig(pop_1_file)
        plt.close()
    
    def find_open_dir(self):
        counter = 0
        while os.path.exists(os.path.join(self.output_dir, str(counter))):
            counter += 1
        self.output_dir = os.path.join(self.output_dir, str(counter))
        print(self.output_dir)
        os.makedirs(self.output_dir, exist_ok=True)