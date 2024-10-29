'''
Initializes game by asking users for inputs and creating environments + agents
Returns: environment
'''
def initialize_game():
    pass


def run():
    env = initialize_game()
    round = 0
    while (round < 100):
        env.play_round()
        env.update_population()
        round+=1

    env.final_stats()
    