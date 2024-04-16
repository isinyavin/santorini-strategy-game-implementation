from game import Game
from board import Board
from command import Invoker, BuildCommand, MoveWorkerCommand, SantoriniCommand 
from strategy import Player, PlayerStrategy, HumanInput

class GameCLI:
    def __init__(self, type1, type2):
        self.game = Game()
        human_strategy = HumanInput()
        if type1 == "human" and type2 == "human":
            self.player1 = Player(human_strategy)
            self.player2 = Player(human_strategy)
        
            
    def run(self):
        while True:
            self.winner_winner_chicken_dinner()
            self.retrieve_all_possible_moves()
            self.print_game_state()
            self.player1.play_turn(self.game)
            self.game.next_turn()
            self.winner_winner_chicken_dinner()
            self.retrieve_all_possible_moves()
            self.print_game_state()
            self.player2.play_turn(self.game)
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
    
    def retrieve_all_possible_moves(self):
        self.game.retrieve_moves()

    def print_game_state(self):
        print(self.game)

    def quit(self):
        exit()
        
if __name__ == "__main__":
    GameCLI("human", "human").run()