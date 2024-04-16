class Worker:
    def __init__(self, letter, x, y):
        if letter in ["A", "B", "Y", "Z"]:
            self.letter = letter
        self.x = x
        self.y = y

    def get_coords(self):
        return self.x, self.y
    
    def set_x(self, x):
        self.x = x
    
    def set_y(self, y):
        self.y = y
    
    def __repr__(self):
        return self.letter
