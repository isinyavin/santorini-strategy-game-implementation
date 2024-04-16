from command import Invoker, BuildCommand, MoveWorkerCommand, SantoriniCommand
import random

class Player:
    def __init__(self, strategy):
        self.strategy = strategy

    def play_turn(self, game):
        return self.strategy.next_move(game)


class PlayerStrategy:
    def next_move(self, game):
        pass

class RandomStrategy(PlayerStrategy):
    def next_move(self, game):
        possible_moves = game.board.enumerate_all_available_moves(game.curr_player_to_move)
        print(possible_moves)
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
        pass

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
            print(worker)
            if worker not in possible_workers:
                print("Not a valid worker")
                continue
            if ((worker in ["Y", "Z"]) and (game.get_curr_player_to_move() == "white")) or ((worker in ["B", "A"] and (game.get_curr_player_to_move() == "blue"))):
                print("That is not your worker")
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
        


