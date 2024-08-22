import json
import random
import pandas as pd
from game import Game
from strategy import Player, RandomStrategy
from board import SantoriniBoard
from worker import WorkerFactory

def serialize_board(board):
    """Converts the board state to a serializable format."""
    return [[{"level": square.level, "worker": str(square.worker)} for square in row] for row in board.squares]

def play_random_game():
    """Plays a random game and stores moves and game outcomes."""
    player1 = Player(RandomStrategy(), "random")
    player2 = Player(RandomStrategy(), "random")
    game = Game(player1, player2, "cli")
    game_data = []

    while not game.check_win():
        board_state = serialize_board(game.board)
        available_moves = game.retrieve_moves()

        if available_moves:
            chosen_move = random.choice(available_moves)

            game_data.append({
                "turn": game.get_turn_num(),
                "player_to_move": game.get_curr_player_to_move(),
                "board_state": board_state,
                "available_moves": available_moves,
                "chosen_move": chosen_move
            })

            game.cur_player_object.play_turn(game, None)
            game.next_turn()

    winner = game.check_win()

    # Add the winner information to all moves in this game
    for move in game_data:
        move["winner"] = winner

    return game_data

def save_game_data(game_data, filename):
    """Saves the game data to a CSV file."""
    df = pd.DataFrame(game_data)
    df.to_csv(filename, index=False)

if __name__ == "__main__":
    all_games_data = []
    for i in range(1000):  
        game_data = play_random_game()
        all_games_data.extend(game_data)

    save_game_data(all_games_data, "raw_santorini_games.csv")
