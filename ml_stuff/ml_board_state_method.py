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
    game = Game(player1, player2, "cli2")
    game_data = []

    while not game.check_win():
        game.cur_player_object.play_turn(game, None)
        game.next_turn()
        board_state = serialize_board(game.board)
        game_data.append(board_state)

    winner = game.check_win()
    total_moves = len(game_data)

    labels = []
    decay_factor = 0.7
    initial_value = 100

    for i in range(total_moves):
        label = max(initial_value * (decay_factor ** (total_moves - 1 - i)),1)
        labels.append(label if winner == "white" else label * -1)


    filtered_game_data = [game_data[i] for i in range(len(labels)) if labels[i] > 1 or labels[i] < -1]
    filtered_labels = [label for label in labels if label > 1 or label < -1]

    return filtered_game_data, filtered_labels

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

    for i in range(100000):  
        game_data, labels = play_random_game()
        all_boards.extend(game_data)
        all_labels.extend(labels)
        print(i)

    save_game_data(all_boards, all_labels, "board_state_data_1k.csv")