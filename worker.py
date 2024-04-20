class WorkerFactory:
    def create_worker(self, name, x, y):
        """Creates worker"""
        return Worker(name, x, y)

class Worker:
    def __init__(self, letter, x, y):
        """Initializes worker"""
        if letter in ["A", "B", "Y", "Z"]:
            self.letter = letter
        self.x = x
        self.y = y

    def get_coords(self):
        """Retrieves coords of the worker"""
        return self.x, self.y
    
    def set_x(self, x):
        """Sets x coord of worker"""
        self.x = x
    
    def set_y(self, y):
        """Sets y coord of the worker"""
        self.y = y
    
    def __repr__(self):
        """Returns represetnation"""
        return self.letter
