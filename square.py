class Square:
    def __init__(self, worker = None, level=0):
        """Initializes square object"""
        self.level = level
        self.worker = worker

    def set_worker(self, worker):
        """Sets the worker"""
        self.worker = worker
    
    def get_worker(self):
        """Retrieves the worker"""
        return self.worker
    
    def get_level(self):
        """Retrieves the level of the square"""
        return self.level
    
    def level_increment(self):
        """Increments level of the square"""
        self.level +=1 
    
    def __repr__(self):
        """Returns repr of the square"""
        return f"{self.level}{self.worker if self.worker else ' '}"