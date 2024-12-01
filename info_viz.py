import os
import matplotlib.pyplot as plt

class Info_viz:
    def __init__(self):
        self.pop_1_over_time = []
        self.pop_2_over_time = []
        self.pop_1_strength_over_time = []
        self.pop_2_strength_over_time = []
        self.output_dir = "saved visuals"
    
    def add_info(self, pop_1_size, pop_2_size, pop_1_strength, pop_2_strength):
        self.pop_1_over_time.append(pop_1_size)
        self.pop_2_over_time.append(pop_2_size)
        self.pop_1_strength_over_time.append(pop_1_strength)
        self.pop_2_strength_over_time.append(pop_2_strength)
    
    def save_info(self):
        self.save_plot_vs_time(self.pop_1_over_time, "Population 1")
        self.save_plot_vs_time(self.pop_2_over_time, "Population 2")
        self.save_plot_vs_time(self.pop_1_strength_over_time, "Pop 1 Strength")
        self.save_plot_vs_time(self.pop_2_strength_over_time, "Pop 2 Strength")
    
    def save_plot_vs_time(self, to_plot, name:str):
        print(to_plot)
        plt.figure()
        plt.plot(to_plot, label=name)
        plt.title(f"{name} Over Time")
        plt.xlabel("Time")
        plt.ylabel(name)
        plt.legend()
        pop_1_file = os.path.join(self.output_dir, f"{name}_over_time.png")
        plt.savefig(pop_1_file)
        plt.close()
