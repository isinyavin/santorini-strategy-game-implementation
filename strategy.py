from command import BuildCommand, MoveWorkerCommand
import random

class Player:
    def __init__(self, strategy):
        """Initializes player object"""
        self.strategy = strategy

    def play_turn(self, game, gamecli):
        """Initiates a move for the player using specified strategy"""
        return self.strategy.next_move(game, gamecli)

class PlayerStrategy:
    def next_move(self, game, gamecli):
        """Interface to implement next move logic below."""
        pass

class RandomStrategy(PlayerStrategy):
    def next_move(self, game, gamecli):
        """Plays random next move based on all possible moves for player"""
        possible_moves = game.board.enumerate_all_available_moves(game.curr_player_to_move)
        if possible_moves:
            move = random.choice(possible_moves)
        move_command = MoveWorkerCommand(game, move[0], move[1])
        game.invoker.store_command(move_command)
        build_command = BuildCommand(game, move[0], move[2])
        game.invoker.store_command(build_command)
        game.invoker.execute_commands()

        if not gamecli.score_output:
             print(f"{move[0]},{move[1]},{move[2]}")
        if gamecli.score_output: 
            print(f"{move[0]},{move[1]},{move[2]} {HeuristicStrategy._total_score(game, game.board)}")

class HeuristicStrategy(PlayerStrategy):
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

            weight1 = 1
            weight2 = 1
            weight3 = 1

            scores.append(weight1*height_score + weight2*center_score + weight3*distance_score)
            
        index = scores.index(max(scores))
        move = possible_moves[index]
        move_command = MoveWorkerCommand(game, move[0], move[1])
        game.invoker.store_command(move_command)
        build_command = BuildCommand(game, move[0], move[2])
        game.invoker.store_command(build_command)
        game.invoker.execute_commands()

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