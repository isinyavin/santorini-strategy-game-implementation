
class SantoriniCommand:
    def execute(self):
        raise NotImplementedError
    
class MoveWorkerCommand(SantoriniCommand):
    def __init__(self, game, worker, direction):
        self.game = game
        self.worker = worker
        self.direction = direction

    def execute(self):
        self.game.move_worker(self.worker, self.direction)

class BuildCommand(SantoriniCommand):
    def __init__(self, game, worker, direction):
        self.game = game
        self.worker = worker
        self.direction = direction

    def execute(self):
        self.game.build(self.worker, self.direction)

class Invoker:
    def __init__(self):
        self._commands = []

    def store_command(self, command):
        self._commands.append(command)

    def execute_commands(self):
        for command in self._commands:
            command.execute()
        self._commands.clear()