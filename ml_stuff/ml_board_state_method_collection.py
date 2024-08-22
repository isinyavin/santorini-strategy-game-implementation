import pandas as pd
import numpy as np
import random
from game import Game
from strategy import Player, RandomStrategy
from board import SantoriniBoard
from worker import WorkerFactory

def serialize_board(board):
    """Converts the board state to a serializable format."""
    return [[{"level": square.level, "worker": str(square.worker)} for square in row] for row in board.squares]

def play_random_game():
    """Plays a random game and stores the board states and outcomes."""
    player1 = Player(RandomStrategy(), "random")
    player2 = Player(RandomStrategy(), "random")
    game = Game(player1, player2, "cli")
    game_data = []

    while not game.check_win():
        board_state = serialize_board(game.board)
        game.cur_player_object.play_turn(game, None)
        game.next_turn()
        game_data.append(board_state)

    winner = game.check_win()

    # Label each board state with the outcome (1 if white wins, 0 otherwise)
    labels = [1 if winner == "white" else 0] * len(game_data)

    return game_data, labels

def save_game_data(board_states, labels, filename):
    """Saves the board states and labels to a CSV file."""
    df = pd.DataFrame({
        "board_state": board_states,
        "label": labels
    })
    df.to_csv(filename, index=False)

if __name__ == "__main__":
    all_boards = []
    all_labels = []

    for i in range(10000):  # Play 10,000 random games
        game_data, labels = play_random_game()
        all_boards.extend(game_data)
        all_labels.extend(labels)

    save_game_data(all_boards, all_labels, "board_state_data.csv")
