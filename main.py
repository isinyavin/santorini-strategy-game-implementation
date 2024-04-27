from game import Game
from strategy import Player, HumanInput, RandomStrategy, HeuristicStrategy
from copy import deepcopy
from momento import Momento, Caretaker
import sys

# sys.setrecursionlimit(2000) # uncomment this if you want to run more than 500 times

class GameInterface:
    def run(self):
        pass

class UndoRedoDecorator(GameInterface):
    def __init__(self, game_cli):
        self.game_cli = game_cli
        self.caretaker = Caretaker(self)

    def run(self):
        """Initiates the game loop when decorator is enabled for undo/redo"""
        while True:
            self.game_cli._retrieve_all_possible_moves()
            self.game_cli._print_game_state()
            self.game_cli._winner_winner_chicken_dinner()
            self._prompt_undo_redo_next()

    def _prompt_undo_redo_next(self):
        valid = False
        while not valid:
            choice = input("undo, redo, or next\n").strip().lower()
            if choice == "undo":
                self.caretaker.undo()
                valid = True
            elif choice == "redo":
                self.caretaker.redo()
                valid = True
            elif choice == "next":
                self.caretaker.backup()
                self.game_cli.game.cur_player_object.play_turn(self.game_cli.game, self.game_cli)
                self.game_cli.game.next_turn()
                valid = True
            else:
                print("Invalid input")

    def restore(self, memento):
        self.game_cli.game = memento.get_saved_state()

class GameCLI():
    def __init__(self, type1, type2, rank):
        """Initializes the GameCLI"""
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
        """Initiates the game input loop."""
        while True:
            self._retrieve_all_possible_moves()
            self._print_game_state()
            self._winner_winner_chicken_dinner()
            self.game.cur_player_object.play_turn(self.game, self)
            self.game.next_turn()

    def _winner_winner_chicken_dinner(self):
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
                self._quit()

    def _retrieve_all_possible_moves(self):
        self.game.retrieve_moves()

    def _print_game_state(self):
        if not self.score_output:
            print(self.game)
        if self.score_output: 
            print(f"{self.game}, {HeuristicStrategy._total_score(self.game, self.game.board)}")

    def _quit(self):
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
