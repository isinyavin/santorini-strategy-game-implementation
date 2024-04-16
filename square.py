class Square:
    def __init__(self, worker = None, level=0):
        self.level = level
        self.worker = worker

    def set_worker(self, worker):
        self.worker = worker
    
    def get_worker(self):
        return self.worker
    
    def get_level(self):
        return self.level
    
    def level_increment(self):
        self.level +=1 
    
    def __repr__(self):
        return f"{self.level}{self.worker if self.worker else ' '}"