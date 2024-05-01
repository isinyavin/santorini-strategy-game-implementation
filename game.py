from board import SantoriniBoard
from command import Invoker
from worker import WorkerFactory

class Game:
    def __init__(self, player1, player2, type):
        """Initialize the game with two players, setting up the board and turn logic."""
        self.invoker = Invoker()
        self.type = type
        self.turn_amount = 1
        self.curr_player_to_move = "white"
        self.board = SantoriniBoard(WorkerFactory())
        self.history = []
        self.future = []
        self.player1 = player1
        self.player2 = player2
        self.cur_player_object = player1
        
    def check_win(self):
        """Check the board state to determine if there is a winning condition."""
        winning_player = self.board.check_if_winning_board()
        if len(self.board.enumerate_all_available_moves(self.curr_player_to_move)) == 0:
            if self.curr_player_to_move == "white":
                return "blue"
            else:
                return "white"
        if str(winning_player) in ["A","B"]:
            return "white"
        if str(winning_player) in ["Y", "Z"]:
            return "blue"
        return None

    def retrieve_moves(self):
        """Retrieve all available moves for the current player."""
        return self.board.enumerate_all_available_moves(self.curr_player_to_move)
    
    def next_turn(self):
        """Advance the game to the next turn, toggling the active player."""
        self.turn_amount += 1
        if self.curr_player_to_move == "white":
            self.curr_player_to_move = "blue"
        else:
            self.curr_player_to_move = "white"
        if self.cur_player_object == self.player1:
            self.cur_player_object = self.player2
        else:
            self.cur_player_object = self.player1
    
    def get_turn_num(self):
        """Return the current turn number."""
        return self.turn_amount
    
    def get_curr_player_to_move(self):
        """Return the color of the current player to move."""
        return self.curr_player_to_move
    
    def get_board(self):
        """Return the current game board."""
        return self.board
    
    def approve_direction_move(self, worker, direction):
        """Check if a move in a given direction is valid and can be executed."""
        if (self.board.is_square_unoccupied_and_valid(worker, direction) and self.board.calculate_distance_jumped(worker, direction) <= 1):
            return True
        else:
            return False
    
    def approve_build_direction(self, worker, direction):
        """Check if a build action in a given direction is valid and can be executed."""
        if (self.board.is_square_unoccupied_and_valid(worker, direction) and self.board.validate_build(worker, direction)):
            return True
        else:
            return False
        
    def move_worker(self, worker, direction):
        """Move a worker in a specified direction on the board."""
        self.board.move_worker_board(worker, direction)

    def build(self, worker, direction):
        """Build on the board in a specified direction using a worker."""
        self.board.build_board(worker, direction)

    def __repr__(self):
        """Return a string representation of the current game state."""
        game_representation = ""
        game_representation += repr(self.board)
        game_representation += f"Turn: {self.turn_amount}, {self.curr_player_to_move} {'(AB)' if self.curr_player_to_move == 'white' else '(YZ)'}"
        return game_representation
