
class SantoriniCommand:
    def execute(self):
        raise NotImplementedError
    
class MoveWorkerCommand(SantoriniCommand):
    def __init__(self, game, worker, direction):
        """Initializeds the MoveWorkerCommandClass"""
        self.game = game
        self.worker = worker
        self.direction = direction

    def execute(self):
        """Executes the action of moving a worker in the specified direction."""
        self.game.move_worker(self.worker, self.direction)

class BuildCommand(SantoriniCommand):
    def __init__(self, game, worker, direction):
        """Initializes the BuildCommand object"""
        self.game = game
        self.worker = worker
        self.direction = direction

    def execute(self):
        """Executes the building action in the given direction."""
        self.game.build(self.worker, self.direction)

class Invoker:
    def __init__(self):
        """Initliazes the invoker."""
        self._commands = []

    def store_command(self, command):
        """Stores a command in the command list to be executed."""
        self._commands.append(command)

    def execute_commands(self):
        """Executes all stored commands and clears the command list afterward."""
        for command in self._commands:
            command.execute()
        self._commands.clear()