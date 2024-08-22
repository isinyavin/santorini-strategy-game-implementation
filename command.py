import time
import time
from tkinter import messagebox

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
    def __init__(self, gui, game):
        """Initliazes the invoker."""
        self._commands = []
        self.gui = gui
        self.game = game

    def store_command(self, command):
        """Stores a command in the command list to be executed."""
        self._commands.append(command)

    def execute_commands(self):
        """Executes all stored commands and clears the command list afterward."""
        for command in self._commands:
            command.execute()
        self._commands.clear()
    
    def slow_execute(self):
        """Executes all stored commands and clears the command list afterward."""
        self.gui.refresh_board()
        self.gui._board.update_button_highlights()
        self.gui._board.clear_highlights() 
        self.gui._window.update() 
    
        for command in self._commands:
            time.sleep(0.4)
            command.execute()
            self.gui.refresh_board()
            self.gui._window.update() 
            time.sleep(0.2)
        if self.game.check_win():
            winner = self.game.check_win()
            #self._disable_buttons()  
            messagebox.showinfo("Game Over", f"{winner} wins!")
            self.gui._window.quit() 
            return 
        self._commands.clear()