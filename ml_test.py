from game import Game
from strategy import Player, RandomStrategy, HeuristicStrategy

def run_game_with_weights(weight1, weight2, weight3):
    random_strategy = RandomStrategy()
    heuristic_strategy = HeuristicStrategy(weight1, weight2, weight3)

    player1 = Player(heuristic_strategy, "heuristic")
    player2 = Player(random_strategy, "random")

    game = Game(player1, player2, "cli2")

    while True:
        if game.check_win():
            return game.check_win()

        game.cur_player_object.play_turn(game, None)
        game.next_turn()

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 4:
        print("Usage: python main_ml_test.py <weight1> <weight2> <weight3>")
        sys.exit(1)

    weight1 = float(sys.argv[1])
    weight2 = float(sys.argv[2])
    weight3 = float(sys.argv[3])

    winner = run_game_with_weights(weight1, weight2, weight3)
    print(f"The winner is: {winner}")
