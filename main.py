from game import Game
from command import Invoker, BuildCommand, MoveWorkerCommand, SantoriniCommand 
from strategy import Player, PlayerStrategy, HumanInput, RandomStrategy, HeuristicStrategy
from copy import deepcopy
from momento import Momento
import sys

class GameInterface:
    def run(self):
        pass

class GameCLI(GameInterface):
    def __init__(self, game, player1, player2):
        self.game = game
        self.player1 = player1
        self.player2 = player2

    def run(self):
        while True:
            pass

class UndoRedoDecorator(GameInterface):
    def __init__(self, game_cli):
        self.game_cli = game_cli
        self.history = []
        self.future = []

    def run(self):
        while True:
            print(len(self.history))
            self.game_cli.retrieve_all_possible_moves()
            self.game_cli.print_game_state()
            self.game_cli.winner_winner_chicken_dinner()
            self.prompt_undo_redo_next()

    def prompt_undo_redo_next(self):
        valid = False
        while not valid:
            choice = input("undo, redo, or next\n").strip().lower()
            if choice == "undo":
                if len(self.history) >= 1: 
                    self.undo()
                    valid = True
                else:
                    print("No more moves to undo.")
            elif choice == "redo":
                if self.future: 
                    self.redo()
                    valid = True
                else:
                    print("No more moves to redo.")
            elif choice == "next":
                valid = True
                self.history.append(Momento(deepcopy(self.game_cli.game)))
                self.game_cli.game.cur_player_object.play_turn(self.game_cli.game)
                self.game_cli.game.next_turn()
                self.future.clear()
            else:
                print("Invalid input")

    def undo(self):
        if self.history:
            self.future.append(Momento(deepcopy(self.game_cli.game)))
            last_state = self.history.pop()
            self.restore_from_memento(last_state)

    def redo(self):
        if self.future:
            self.history.append(Momento(deepcopy(self.game_cli.game)))
            next_state = self.future.pop()
            self.restore_from_memento(next_state)

    def restore_from_memento(self, memento):
        self.game_cli.game = memento.get_saved_state()


class GameCLI:
    def __init__(self, type1, type2, rank):

        human_strategy = HumanInput()
        random_strategy = RandomStrategy()
        heuristic_strategy = HeuristicStrategy()

        if type1 == "human": player1 = Player(human_strategy)
        if type1 == "heuristic": player1 = Player(heuristic_strategy)
        if type1 == "random": player1 = Player(random_strategy)
        
        if type2 == "human": player2 = Player(human_strategy)
        if type2 == "heuristic":player2 = Player(heuristic_strategy)
        if type2 == "random":player2 = Player(random_strategy)

        if rank == True: 
            self.score_output = True
        else:
            self.score_output = False
    
        self.game = Game(player1, player2)
        
    def run(self):
        while True:
            self.retrieve_all_possible_moves()
            self.print_game_state()
            self.winner_winner_chicken_dinner()
            self.game.cur_player_object.play_turn(self.game)
            self.game.next_turn()

    def winner_winner_chicken_dinner(self):
        winner = self.game.check_win()
        if winner != None:
            print(f"{winner} has won")
            check = input("Play again?\n")
            if check.lower() == "yes":
                
                game_cli = GameCLI(white_player_type, blue_player_type, score_display_bool)

                if not undo_redo_bool:
                    game_cli.run()
                else:
                    undo_redo_cli = UndoRedoDecorator(game_cli)
                    undo_redo_cli.run()

            else:
                self.quit()

    def retrieve_all_possible_moves(self):
        self.game.retrieve_moves()

    def print_game_state(self):
        if not self.score_output:
            print(self.game)
        if self.score_output: 
            print(f"{self.game}, {HeuristicStrategy.total_score(self.game, self.game.board)}")

    def quit(self):
        exit()
        
if __name__ == "__main__":
    white_player_type = 'human'
    blue_player_type = 'human'
    undo_redo_enabled = 'off'
    score_display_enabled = 'off'
    
    if len(sys.argv) > 1:
        white_player_type = sys.argv[1]
    if len(sys.argv) > 2:
        blue_player_type = sys.argv[2]
    if len(sys.argv) > 3:
        undo_redo_enabled = sys.argv[3]
    if len(sys.argv) > 4:
        score_display_enabled = sys.argv[4]

    undo_redo_bool = undo_redo_enabled.lower() == 'on'
    score_display_bool = score_display_enabled.lower() == 'on'

    game_cli = GameCLI(white_player_type, blue_player_type,score_display_bool)

    if not undo_redo_bool:
        game_cli.run()
    else:
        undo_redo_cli = UndoRedoDecorator(game_cli)
        undo_redo_cli.run()
