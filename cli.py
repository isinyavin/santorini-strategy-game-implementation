from game import Game
from board import Board
from command import Invoker, BuildCommand, MoveWorkerCommand, SantoriniCommand 
from strategy import Player, PlayerStrategy, HumanInput, RandomStrategy, HeuristicStrategy

class GameCLI:
    def __init__(self, type1, type2):
        human_strategy = HumanInput()
        random_strategy = RandomStrategy()
        heuristic_strategy = HeuristicStrategy()
        self.undo_redo_next = False
        if type1 == "human" and type2 == "human":
            player1 = Player(heuristic_strategy)
            player2 = Player(heuristic_strategy)
        self.game = Game(player1, player2)
        
    def run(self):
        self.game.history.append(self.game.board.save_to_momento())
        while True:
            self.retrieve_all_possible_moves()
            self.print_game_state()
            self.winner_winner_chicken_dinner()
            print(len(self.game.history))
            if self.undo_redo_next: self.prompt_undo_redo_next()
            self.game.cur_player_object.play_turn(self.game)
            self.game.history.append(self.game.board.save_to_momento())
            self.game.future.clear()
            self.game.next_turn()

    def winner_winner_chicken_dinner(self):
        winner = self.game.check_win()
        if winner != None:
            print(f"{winner} has won")
            check = input("Play again?\n")
            if check.lower() == "yes":
                self.game = Game()
                self.run()
            else:
                self.quit()

    def prompt_undo_redo_next(self):
        valid = False
        while not valid:
            choice = input("undo, redo, or next\n").strip().lower()
            if choice == "undo":
                if len(self.game.history) >= 1: 
                    self.game.undo()
                    self.print_game_state() 
                    valid = True
                else:
                    print("No more moves to undo.")
            elif choice == "redo":
                if self.game.future: 
                    self.game.redo()
                    self.print_game_state() 
                    valid = True
                else:
                    print("No more moves to redo.")
            elif choice == "next":
                valid = True
            
            else:
                print("Invalid input")

    
    def retrieve_all_possible_moves(self):
        self.game.retrieve_moves()

    def print_game_state(self):
        print(self.game)

    def quit(self):
        exit()
        
if __name__ == "__main__":
    GameCLI("human", "human").run()