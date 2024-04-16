
class SantoriniSquareIterator:
    def __init__(self, board):
        self.board = board
        self.outer_index = 0
        self.inner_index = 0
        self.len_outer = 4

    def __iter__(self):
        return self

    def __next__(self):
        if self.outer_index >= self.len_outer:
            raise StopIteration

        current_list = self.board[self.outer_index]
        if self.inner_index >= len(current_list):
            self.outer_index += 1
            self.inner_index = 0
            return self.__next__()

        element = current_list[self.inner_index]
        self.inner_index += 1
        return element

