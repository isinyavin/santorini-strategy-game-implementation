from copy import deepcopy
class Momento:
    def __init__(self, state):
        """Initializes momento object"""
        self._state = state

    def get_saved_state(self):
        """Returns saved state of the object"""
        return self._state

class Caretaker:
    def __init__(self, originator):
        """Initializes the caretaker"""
        self._history = []
        self._future = []
        self._originator = originator

    def backup(self):
        """Backups the current state of originator"""
        self._history.append(Momento(deepcopy(self._originator.game_cli.game)))
        self._future.clear()

    def undo(self):
        """Undos the state of the game"""
        if not self._history:
            return
        self._future.append(Momento(deepcopy(self._originator.game_cli.game)))
        momento = self._history.pop()
        self._originator.restore(momento)

    def redo(self):
        """Redos the state of the game"""
        if not self._future:
            return
        self._history.append(Momento(deepcopy(self._originator.game_cli.game)))
        momento = self._future.pop()
        self._originator.restore(momento)


    

