from board import Board
from command import Invoker

class Game:
    def __init__(self, player1, player2):
        self.invoker = Invoker()
        self.turn_amount = 0
        self.curr_player_to_move = "white"
        self.board = Board()
        self.history = []
        self.future = []
        self.player1 = player1
        self.player2 = player2
        self.cur_player_object = player1
        
    def check_win(self):
        winning_player = self.board.check_if_winning_board()
        print(winning_player)
        if str(winning_player) in ["A","B"]:
            return "white"
        if str(winning_player) in ["Y", "Z"]:
            return "blue"
        return None

    def retrieve_moves(self):
        return self.board.enumerate_all_available_moves(self.curr_player_to_move)
    
    def next_turn(self):
        self.turn_amount += 1
        if self.curr_player_to_move == "white":
            self.curr_player_to_move = "blue"
        else:
            self.curr_player_to_move = "white"
        if self.cur_player_object == self.player1:
            self.cur_player_object = self.player2
        else:
            self.cur_player_object == self.player1
    
    def get_turn_num(self):
        return self.turn_amount
    
    def get_curr_player_to_move(self):
        return self.curr_player_to_move
    
    def get_board(self):
        return self.board
    
    def approve_direction_move(self, worker, direction):
        if (self.board.is_square_unoccupied_and_valid(worker, direction) and self.board.calculate_distance_jumped(worker, direction) <= 1):
            return True
        else:
            return False
    
    def approve_build_direction(self, worker, direction):
        if (self.board.is_square_unoccupied_and_valid(worker, direction) and self.board.validate_build(worker, direction)):
            return True
        else:
            return False
        
    def move_worker(self, worker, direction):
        self.board.move_worker_board(worker, direction)

    def build(self, worker, direction):
        self.board.build_board(worker, direction)

    def undo(self):
        if len(self.history) >= 1: 
            memento = self.history.pop()
            self.future.append(memento)
            self.board.restore_from_memento(self.history[-1]) if len(self.history) > 1 else self.board.restore_from_memento(self.history[0])
    
    def redo(self):
        if self.future:
            memento = self.future.pop()
            self.history.append(memento)
            self.board.restore_from_memento(memento)


    def __repr__(self):
        game_representation = ""
        game_representation += repr(self.board)
        game_representation += f"Turn: {self.turn_amount}, {self.curr_player_to_move} {'(AB)' if self.curr_player_to_move == 'white' else '(YZ)'}"
        return game_representation


