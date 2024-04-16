




from command import Invoker, BuildCommand, MoveWorkerCommand, SantoriniCommand
import random

class Player:
    def __init__(self, strategy):
        self.strategy = strategy

    def play_turn(self, game):
        return self.strategy.next_move(game)


class PlayerStrategy:
    def next_move(self, game):
        c

class RandomStrategy(PlayerStrategy):
    def next_move(self, game):
        possible_moves = game.board.enumerate_all_available_moves(game.curr_player_to_move)
        if possible_moves:
            move =  random.choice(possible_moves)
        move_command = MoveWorkerCommand(game, move[0], move[1])
        game.invoker.store_command(move_command)
        build_command = BuildCommand(game, move[0], move[2])
        game.invoker.store_command(build_command)
        game.invoker.execute_commands()
        print(f"{move[0]},{move[1]},{move[2]}")

class HeuristicStrategy(PlayerStrategy):
    def next_move(self, game):
        possible_moves = game.board.enumerate_all_available_moves(game.curr_player_to_move)
        scores = []
        for moves in possible_moves:
            momento = game.board.save_to_momento()
            board = momento.get_saved_state()
            board.move_worker_board(moves[0], moves[1])
            board.build_board(moves[0], moves[2])
            height_score = HeuristicStrategy.height_calculate(board, game)
            weight1 = 1
            weight2 = 1
            weight3 = 1
            scores.append(weight1*height_score)
        print(scores)
        index = scores.index(max(scores))
        actual_move = possible_moves[index]
        move_command = MoveWorkerCommand(game, actual_move[0], actual_move[1])
        game.invoker.store_command(move_command)
        build_command = BuildCommand(game, actual_move[0], actual_move[2])
        game.invoker.store_command(build_command)
        game.invoker.execute_commands()
        print(f"Optimized moves: {actual_move[0]},{actual_move[1]},{actual_move[2]}")
        

    def height_calculate(board, game):
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


class HumanInput(PlayerStrategy):
    def next_move(self, game):
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
        print(f"{worker},{direction},{build_direction}")
        


