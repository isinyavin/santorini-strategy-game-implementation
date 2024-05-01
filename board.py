from square import Square
from iterator import SantoriniSquareIterator
from momento import Momento
from copy import deepcopy

class AbstractBoard:
    def __init__(self, num_rows, num_cols):
        """Initialize an abstract board with a given number of rows and columns filled with Square instances."""
        self.squares = [[Square() for i in range(num_rows)] for i in range(num_cols)]

class SantoriniBoard(AbstractBoard):
    def __init__(self, worker_factory):
        """Initialize the SantoriniBoard with specific worker placements using a worker factory."""
        super().__init__(5, 5)
        self.workerY = worker_factory.create_worker("Y", 1, 1)
        self.workerA = worker_factory.create_worker("A", 3, 1)
        self.workerB = worker_factory.create_worker("B", 1, 3)
        self.workerZ = worker_factory.create_worker("Z", 3, 3)

        self.squares[1][1].set_worker(self.workerY)
        self.squares[3][1].set_worker(self.workerB)
        self.squares[1][3].set_worker(self.workerA)
        self.squares[3][3].set_worker(self.workerZ)
        
    def check_if_winning_board(self):
        """Check all squares to determine if any worker has reached the third level, indicating a win."""
        iteratable_board = SantoriniSquareIterator(self.squares)
        for square in iteratable_board:
            if square.level == 3 and square.worker != None:
                return square.worker
        
    def _get_new_coords_from_direction(self, worker_letter, direction):
        worker = self._return_worker_from_letter(worker_letter)
        x_old, y_old = worker.get_coords()
        moved_coords = self.find_new_coords(x_old, y_old, direction)
        return moved_coords, worker

    def is_square_unoccupied_and_valid(self, worker, direction):
        """Check if the square in the given direction is unoccupied and valid for movement or building."""
        moved_coords, worker = self._get_new_coords_from_direction(worker, direction)
        x, y = moved_coords
        if not(x >= 0 and x <= 4 and y >= 0 and y <= 4):
            return False
        target_square = self.squares[moved_coords[0]][moved_coords[1]]
        if (target_square.get_worker() == None) and (target_square.get_level() != 4):
            return True
        else:
            return False
        
    def _return_worker_from_letter(self, worker):
        if worker == "A": return self.workerA
        if worker == "B": return self.workerB
        if worker == "Z": return self.workerZ
        if worker == "Y": return self.workerY

    def calculate_distance_jumped(self, worker, direction):
        """Calculate the difference in level between the worker's current square and the target square."""
        moved_coords, worker = self._get_new_coords_from_direction(worker, direction)
        x, y = moved_coords
        x_old,y_old = worker.get_coords()
        old_level = self.squares[x_old][y_old].get_level()
        new_level = self.squares[x][y].get_level()
        return new_level - old_level

    def validate_build(self, worker, direction):
        """Validate if a building move is possible at the target square."""
        moved_coords, worker = self._get_new_coords_from_direction(worker, direction)
        x, y = moved_coords
        level_of_target = self.squares[x][y].get_level()
        if (level_of_target < 4):
            return True
        else:
            return False
        
    def move_worker_board(self, worker, direction):
        """Move the specified worker to a new square in the given direction."""
        moved_coords, worker = self._get_new_coords_from_direction(worker, direction)
        x, y = moved_coords
        x_old,y_old = worker.get_coords()
        worker.set_x(x)
        worker.set_y(y)
        self.squares[x][y].set_worker(worker)
        self.squares[x_old][y_old].set_worker(None)

    def build_board(self, worker, direction):
        """Increment the level of the building at the square in the given direction."""
        moved_coords, worker = self._get_new_coords_from_direction(worker, direction)
        x, y = moved_coords
        self.squares[x][y].level_increment()

    def find_worker_coords(self, selected_worker):
        """Find the coordinates of the selected worker on the board."""
        worker = self._return_worker_from_letter(selected_worker)
        return worker.get_coords()

    @staticmethod
    def find_new_coords(x, y, direction):
        """Static method to find new coordinates based on the current position and direction of movement."""
        if direction == "n": return x-1, y
        if direction == "s": return x +1,y
        if direction == "w": return x, y -1
        if direction == "e": return x, y+1
        if direction == "nw": return x-1,y-1
        if direction == "ne": return x-1,y+1
        if direction == "sw": return x+1,y-1
        if direction == "se": return x+1,y+1

    @staticmethod
    def find_new_coords2(x, y, direction):
        """Static method to find new coordinates based on the current position and direction of movement."""
        if direction == "w": return x-1, y
        if direction == "e": return x +1,y
        if direction == "n": return x, y -1
        if direction == "s": return x, y+1
        if direction == "nw": return x-1,y-1
        if direction == "sw": return x-1,y+1
        if direction == "ne": return x+1,y-1
        if direction == "se": return x+1,y+1
    

    def enumerate_all_available_moves(self, player):
        """Enumerate all possible legal moves for a given player based on the current board state."""
        if player == "white":
            workers = ["A", "B"]
        if player =="blue":
            workers = ["Z", "Y"]
        possible_moves = []
        possible_directions = ["n", "e", "ne", "se", "s", "sw", "w", "nw"]
        move_forward_and_back = {"n":"s", "s":"n", "e":"w", "w":"e", "nw":"se", "se":"nw", "ne":"sw", "sw":"ne"}
        for worker in workers:
            valid_move_directions = []
            for direction in possible_directions:
                if self.is_square_unoccupied_and_valid(str(worker), direction) and self.calculate_distance_jumped(str(worker), direction) <= 1:
                    valid_move_directions.append(direction)
            for valid_direction in valid_move_directions:
                self.move_worker_board(str(worker), valid_direction)
                for build_direction in possible_directions:
                    if (self.is_square_unoccupied_and_valid(str(worker), build_direction) and self.validate_build(str(worker), build_direction)):
                        possible_moves.append([worker, valid_direction, build_direction])

                self.move_worker_board(worker, move_forward_and_back[valid_direction])
            
        return possible_moves
                
    def save_to_momento(self):
        """Save the current state of the board to a memento for undo functionality."""
        return Momento(deepcopy(self))

    def restore_from_memento(self, memento):
        """Restore the board state from a memento."""
        self = memento.get_saved_state()

    def __repr__(self):
        """Return a string representation of the board's current state."""
        board_representation = "+--+--+--+--+--+\n"
        for row in self.squares:
            board_representation += "|" + "|".join(repr(square) for square in row) + "|\n"
            board_representation += "+--+--+--+--+--+\n"
        return board_representation