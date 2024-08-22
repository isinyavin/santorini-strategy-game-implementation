from game import Game
from strategy import Player, RandomStrategy, HeuristicStrategy
import random

def run_game_with_weights(weight1, weight2, weight3):
    random_strategy = RandomStrategy()
    heuristic_strategy = HeuristicStrategy(weight1, weight2, weight3)

    player1 = Player(heuristic_strategy, "heuristic")
    player2 = Player(random_strategy, "random")

    game = Game(player1, player2, "cli2")

    while True:
        if game.check_win():
            print(game.check_win())
            return game.check_win()

        game.cur_player_object.play_turn(game, None)
        game.next_turn()

def simulate_games(weight1, weight2, weight3, num_games=10000):
    heuristic_wins = 0

    for _ in range(num_games):
        winner = run_game_with_weights(weight1, weight2, weight3)
        if winner == "white":
            heuristic_wins += 1

    win_percentage = (heuristic_wins / num_games) * 100
    return win_percentage

def optimize_weights(num_iterations=10000, num_games_per_simulation=100):
    best_weights = [3, 2, 1]  # Initial weights
    best_win_percentage = 0


    with open("optimization_results.txt", "a") as f:
        for iteration in range(num_iterations):

            weight1 = random.uniform(1, 5)
            weight2 = random.uniform(1, 5)
            weight3 = random.uniform(1, 5)

            win_percentage = simulate_games(weight1, weight2, weight3, num_games=num_games_per_simulation)

            f.write(f"Iteration {iteration + 1}/{num_iterations}: Weights: [{weight1:.2f}, {weight2:.2f}, {weight3:.2f}] - Win Percentage: {win_percentage:.2f}%\n")

            print(f"Iteration {iteration + 1}/{num_iterations}: Weights: [{weight1:.2f}, {weight2:.2f}, {weight3:.2f}] - Win Percentage: {win_percentage:.2f}%")

            if win_percentage > best_win_percentage:
                best_win_percentage = win_percentage
                best_weights = [weight1, weight2, weight3]
                print(best_weights)
                print(best_win_percentage)
                f.write(f"New best weights found: {best_weights} with win percentage: {best_win_percentage:.2f}%\n")

        f.write(f"\nOptimization complete. Best weights: {best_weights} with win percentage: {best_win_percentage:.2f}%\n")

if __name__ == "__main__":
    optimize_weights()