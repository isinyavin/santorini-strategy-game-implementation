from command import BuildCommand, MoveWorkerCommand
from tensorflow.keras.models import load_model
import random
import numpy as np
from copy import deepcopy

class Player:
    def __init__(self, strategy, type):
        """Initializes player object"""
        self.strategy = strategy
        self.type = type

    def play_turn(self, game, gamecli):
        """Initiates a move for the player using specified strategy"""
        return self.strategy.next_move(game, gamecli)

class PlayerStrategy:
    def next_move(self, game, gamecli):
        """Interface to implement next move logic below."""
        pass

class RandomStrategy(PlayerStrategy):
    def next_move(self, game, gamecli):
        """Plays random next move based on all possible moves for player."""
        possible_moves = game.board.enumerate_all_available_moves(game.curr_player_to_move)
        
        if possible_moves:
            move = random.choice(possible_moves)  
            self.execute_move(game, move, gamecli)

    def play_given_move(self, game, move, gamecli):
        """Executes a specific move given as input."""
        possible_moves = game.board.enumerate_all_available_moves(game.curr_player_to_move)
        if move in possible_moves:
            self.execute_move(game, move, gamecli)
        else:
            print("Invalid move provided.")

    def execute_move(self, game, move, gamecli):
        """Executes a move in the game."""
        move_command = MoveWorkerCommand(game, move[0], move[1])
        game.invoker.store_command(move_command)
        build_command = BuildCommand(game, move[0], move[2])
        game.invoker.store_command(build_command)
        
        if game.type == "gui":
            game.invoker.slow_execute()
        else:
            game.invoker.execute_commands()

        if game.type == "cli":
            if not gamecli or not gamecli.score_output:
                print(f"{move[0]},{move[1]},{move[2]}")
            if gamecli and gamecli.score_output:
                print(f"{move[0]},{move[1]},{move[2]} {HeuristicStrategy._total_score(game, game.board)}")


class HeuristicStrategy(PlayerStrategy):
    def __init__(self, weight1=3, weight2=2, weight3=1):
        """Initializes with the provided weights for each factor."""
        self.weight1 = weight1
        self.weight2 = weight2
        self.weight3 = weight3

    def next_move(self, game, gamecli):
        """Plays next move based on heuristic strategy"""
        possible_moves = game.board.enumerate_all_available_moves(game.curr_player_to_move)
        scores = []
        for moves in possible_moves:
            momento = game.board.save_to_momento()
            board = momento.get_saved_state()
            board.move_worker_board(moves[0], moves[1])
            board.build_board(moves[0], moves[2])
            height_score = HeuristicStrategy._height_calculate(board, game)
            center_score = HeuristicStrategy._center_calculate(board, game)
            distance_score = HeuristicStrategy._distance_calculate(board, game)

            scores.append(
                self.weight1 * height_score +
                self.weight2 * center_score +
                self.weight3 * distance_score
            )
            
        index = scores.index(max(scores))
        move = possible_moves[index]
        move_command = MoveWorkerCommand(game, move[0], move[1])
        game.invoker.store_command(move_command)
        build_command = BuildCommand(game, move[0], move[2])
        game.invoker.store_command(build_command)

        if game.type == "gui":
            game.invoker.slow_execute()
        else:
            game.invoker.execute_commands()


        if game.type == "cli":
            if not gamecli.score_output:
                print(f"{move[0]},{move[1]},{move[2]}")
            if gamecli.score_output: 
                print(f"{move[0]},{move[1]},{move[2]} {HeuristicStrategy._total_score(game, game.board)}")
        
    def _total_score(game, board): 
        height_score = HeuristicStrategy._height_calculate(board, game)
        center_score = HeuristicStrategy._center_calculate(board, game)
        distance_score = HeuristicStrategy._distance_calculate(board, game)
        return f"({height_score}, {center_score}, {distance_score})"
        
    def _height_calculate(board, game):
        height = 0
        if game.cur_player_object == game.player1:
            workers = ["A","B"]
        if game.cur_player_object == game.player2:
            workers = ["Z", "Y"]
        for line in board.squares:
            for square in line:
                if str(square.worker) in workers:
                    height += square.level
        return height
    
    
    def _distance_calculate(board, game):
        if game.cur_player_object == game.player1:
            workers = ["A", "B"]
            others = ["Y", "Z"]
        elif game.cur_player_object == game.player2:
            workers = ["Z", "Y"]
            others = ["A", "B"]

        distance_a = 0
        distance_b = 0
        distance_c = 0
        distance_d = 0
            
        for first_worker_row in board.squares:
            for first_worker_column in first_worker_row:
                if str(first_worker_column.worker) in workers:

                    for second_worker_row in board.squares:
                        for second_worker_column in second_worker_row:
                            if str(second_worker_column.worker) in others:

                                y1 = board.squares.index(first_worker_row)
                                y2 = board.squares.index(second_worker_row)

                                x1 = first_worker_row.index(first_worker_column)
                                x2 = second_worker_row.index(second_worker_column)

                                distance = max(abs(y1 - y2), abs(x1 - x2))

                                if str(first_worker_column.worker) in ['A','Y']:
                                    if distance_a == 0:
                                        distance_a += distance
                                    else:
                                        distance_b += distance
                                elif str(first_worker_column.worker) in ['B','Z']:
                                    if distance_c == 0:
                                        distance_c += distance
                                    else:
                                        distance_d += distance

        final_distance = min(distance_a, distance_c) + min(distance_b, distance_d)
        return 8 - final_distance


    def _center_calculate(board, game):
        center_score = 0
        if game.cur_player_object == game.player1:
            workers = ["A","B"]
        if game.cur_player_object == game.player2:
            workers = ["Z", "Y"]

        center_score = 0

        for first_worker_row in board.squares:
            for first_worker_column in first_worker_row:
                if str(first_worker_column.worker) in workers:

                    x1 = first_worker_row.index(first_worker_column)
                    y1 = board.squares.index(first_worker_row)

                    if x1 == 2 and y1 == 2:
                        center_score += 2
                    elif x1 == 1 and y1 == 1 or y1 == 2 or y1 == 3:
                        center_score += 1
                    elif x1 == 2 and y1 == 1 or y1 == 3:
                        center_score += 1
                    elif x1 == 3 and y1 == 1 or y1 == 2 or y1 == 3:
                        center_score += 1

        return center_score

class HumanInput(PlayerStrategy):
    def next_move(self, game, gamecli):
        """Retrives next move based on human input"""
        move_forward_and_back = {"n":"s", "s":"n", "e":"w", "w":"e", "nw":"se", "se":"nw", "ne":"sw", "sw":"ne"}
        possible_workers  = ["Y", "Z", "B", "A"]
        possible_directions = ["n", "e", "ne", "se", "s", "sw", "w", "nw"]

        approved = False
        approved2 = False
        approved3 = False
        
        while approved == False:
            worker = input("Select a worker to move\n")
            if worker not in possible_workers:
                print("Not a valid worker")
                continue
            if ((worker in ["Y", "Z"]) and (game.get_curr_player_to_move() == "white")) or ((worker in ["B", "A"] and (game.get_curr_player_to_move() == "blue"))):
                print("That is not your worker")
                continue
            possible_moves = game.board.enumerate_all_available_moves(game.curr_player_to_move)
            if len(possible_moves) > 0:
                eligible_workers = []
                for move in possible_moves:
                    eligible_workers.append(move[0])
                options = set(eligible_workers)
                if worker not in options:
                    print("Worker cannot move")
                    continue
                else:
                    approved = True
            else:
                approved = True

        while approved2 == False:
            direction = input("Select a direction to move (n, ne, e, se, s, sw, w, nw)\n")
            if direction not in possible_directions:
                print("Not a valid direction")
                continue
            if game.approve_direction_move(worker, direction) == False:
                print(f"Cannot move {direction}")
                continue
            else:
                game.move_worker(worker, direction)
                move_command = MoveWorkerCommand(game, worker, direction)
                game.invoker.store_command(move_command)
                approved2 = True

        while approved3 == False:
            build_direction = input("Select a direction to build (n, ne, e, se, s, sw, w, nw)\n")
            if build_direction not in possible_directions:
                print("Not a valid direction")
                continue
            if game.approve_build_direction(worker, build_direction) == False:
                print(f"Cannot build {build_direction}")
                continue
            else:
                build_command = BuildCommand(game, worker, build_direction)
                game.invoker.store_command(build_command)
                approved3 = True

        game.board.move_worker_board(worker, move_forward_and_back[direction])
        game.invoker.execute_commands()
        
        if not gamecli.score_output:
             print(f"{worker},{direction},{build_direction}")
        if gamecli.score_output: 
            print(f"{worker},{direction},{build_direction} {HeuristicStrategy._total_score(game, game.board)}")


class MLStrategy(PlayerStrategy):
    def __init__(self, model_path):
        """Initialize the strategy with a pre-trained model."""
        self.model = load_model(model_path, compile=False)
        self.model.compile(optimizer='adam', loss='mse')
        self.turn_counter = 0  # Track the number of turns

    def next_move(self, game, gamecli):
        """Plays the next move based on the model's prediction or heuristic strategy."""
        self.turn_counter += 1

        # Use heuristic strategy for the first 10 turns (5 AI turns)
        if self.turn_counter <= 5:
            print(f"Using heuristic strategy for turn {self.turn_counter}")
            self.heuristic_strategy(game, gamecli)
        else:
            print(f"Using ML strategy for turn {self.turn_counter}")
            self.ml_strategy(game, gamecli)

    def heuristic_strategy(self, game, gamecli):
        """Heuristic-based move selection."""
        possible_moves = game.board.enumerate_all_available_moves(game.curr_player_to_move)
        scores = []
        for move in possible_moves:
            cloned_game = deepcopy(game)
            cloned_game.move_worker(move[0], move[1])
            cloned_game.build(move[0], move[2])
            
            height_score = HeuristicStrategy._height_calculate(cloned_game.board, game)
            center_score = HeuristicStrategy._center_calculate(cloned_game.board, game)
            distance_score = HeuristicStrategy._distance_calculate(cloned_game.board, game)
            
            score = height_score * 3 + center_score * 2 + distance_score
            scores.append(score)
        
        best_move = possible_moves[scores.index(max(scores))]
        self.execute_move(game, best_move, gamecli)

    def ml_strategy(self, game, gamecli):
        """ML-based move selection."""
        possible_moves = game.board.enumerate_all_available_moves(game.curr_player_to_move)
        best_move = None
        best_probability = 1

        for move in possible_moves:
            board_tensor = self.generate_board_tensor(game, move)
            
            probability = self.model.predict(np.array([board_tensor]))[0][0]
            print(f"Move: {move}, Q-Score: {probability}")

            if probability < best_probability:
                best_probability = probability
                best_move = move
        
        if best_move:
            self.execute_move(game, best_move, gamecli)

    def generate_board_tensor(self, game, move):
        """Generates a 5x5x5 tensor representing the board state after making the given move."""
        cloned_game = deepcopy(game)
        cloned_game.move_worker(move[0], move[1])
        cloned_game.build(move[0], move[2])

        board_tensor = np.zeros((5, 5, 5))

        for i, row in enumerate(cloned_game.board.squares):
            for j, square in enumerate(row):
                board_tensor[i, j, 0] = square.level
                if square.worker == "A":
                    board_tensor[i, j, 1] = 1
                elif square.worker == "B":
                    board_tensor[i, j, 2] = 1
                elif square.worker == "Y":
                    board_tensor[i, j, 3] = 1
                elif square.worker == "Z":
                    board_tensor[i, j, 4] = 1

        return board_tensor

    def execute_move(self, game, move, gamecli):
        """Executes the chosen move in the game."""
        move_command = MoveWorkerCommand(game, move[0], move[1])
        game.invoker.store_command(move_command)
        build_command = BuildCommand(game, move[0], move[2])
        game.invoker.store_command(build_command)
        
        if game.type == "gui":
            game.invoker.slow_execute()
        else:
            game.invoker.execute_commands()

        if game.type == "cli":
            if not gamecli or not gamecli.score_output:
                print(f"{move[0]},{move[1]},{move[2]}")
            if gamecli and gamecli.score_output:
                print(f"{move[0]},{move[1]},{move[2]} {HeuristicStrategy._total_score(game, game.board)}")



class MLStrategy_Vector(PlayerStrategy):
    def __init__(self, model_path):
        """Initialize the strategy with a pre-trained model."""
        self.model = load_model(model_path)

    def next_move(self, game, gamecli):
        """Plays the next move based on the model's prediction."""
        possible_moves = game.board.enumerate_all_available_moves(game.curr_player_to_move)
        best_move = None
        best_probability = -1
        
        for move in possible_moves:
            features = self.generate_features(game, move)
            
            probability = self.model.predict(np.array([features]))[0][0] 
            print(probability)
            
            if probability > best_probability:
                best_probability = probability
                best_move = move
        
        if best_move:
            self.execute_move(game, best_move, gamecli)

    def generate_features(self, game, move):
        """Generates the feature vector for a given game state and move."""
        board_state = self.serialize_board(game.board)
        worker = move[0]
        move_direction = move[1]
        build_direction = move[2]

        board_features = []
        for row in board_state:
            for square in row:
                board_features.append(square["level"])
                board_features.append(self.encode_worker(square["worker"]))

        move_features = [
            self.encode_worker(worker),
            self.encode_direction(move_direction),
            self.encode_direction(build_direction)
        ]

        # Combine board features and move information
        return np.array(board_features + move_features)

    def serialize_board(self, board):
        """Converts the board state to a serializable format."""
        return [[{"level": square.level, "worker": str(square.worker)} for square in row] for row in board.squares]

    def encode_worker(self, worker):
        """Encodes the worker as a numerical feature."""
        encoding = {"A": 0, "B": 1, "Y": 2, "Z": 3}
        return encoding.get(worker, -1)  # -1 for empty or invalid workers

    def encode_direction(self, direction):
        """Encodes a direction as a numerical feature."""
        encoding = {"n": 0, "ne": 1, "e": 2, "se": 3, "s": 4, "sw": 5, "w": 6, "nw": 7}
        return encoding.get(direction, -1)  # -1 for invalid directions

    def execute_move(self, game, move, gamecli):
        """Executes a move in the game."""
        move_command = MoveWorkerCommand(game, move[0], move[1])
        game.invoker.store_command(move_command)
        build_command = BuildCommand(game, move[0], move[2])
        game.invoker.store_command(build_command)
        
        if game.type == "gui":
            game.invoker.slow_execute()
        else:
            game.invoker.execute_commands()

        if game.type == "cli":
            if not gamecli or not gamecli.score_output:
                print(f"{move[0]},{move[1]},{move[2]}")
            if gamecli and gamecli.score_output:
                print(f"{move[0]},{move[1]},{move[2]} {HeuristicStrategy._total_score(game, game.board)}")
