class Memento:
    def __init__(self, state):
        self._state = state

    def get_saved_state(self):
        return self._state
