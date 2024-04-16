class State:
    def handle(self, type1, type2, players):
        pass

class HumanHumanState(State):
    def handle(self, type1, type2, players):
        players['player1'] = Player(human_strategy)
        players['player2'] = Player(human_strategy)
        return players

class HumanRandomState(State):
    def handle(self, type1, type2, players):
        players['player1'] = Player(human_strategy)
        players['player2'] = Player(random_strategy)
        return players

class RandomHumanState(State):
    def handle(self, type1, type2, players):
        players['player1'] = Player(random_strategy)
        players['player2'] = Player(human_strategy)
        return players

class HumanHeuristicState(State):
    def handle(self, type1, type2, players):
        players['player1'] = Player(human_strategy)
        players['player2'] = Player(heuristic_strategy)
        return players

class HeuristicHumanState(State):
    def handle(self, type1, type2, players):
        players['player1'] = Player(heuristic_strategy)
        players['player2'] = Player(human_strategy)
        return players

class RandomRandomState(State):
    def handle(self, type1, type2, players):
        players['player1'] = Player(random_strategy)
        players['player2'] = Player(random_strategy)
        return players

class HeuristicHeuristicState(State):
    def handle(self, type1, type2, players):
        players['player1'] = Player(heuristic_strategy)
        players['player2'] = Player(heuristic_strategy)
        return players

class InvalidState(State):
    def handle(self, type1, type2, players):
        print("please provide a valid player type")
        return players

class Context:
    def __init__(self):
        self.states = {
            ('human', 'human'): HumanHumanState(),
            ('human', 'random'): HumanRandomState(),
            ('random', 'human'): RandomHumanState(),
            ('human', 'heuristic'): HumanHeuristicState(),
            ('heuristic', 'human'): HeuristicHumanState(),
            ('random', 'random'): RandomRandomState(),
            ('heuristic', 'heuristic'): HeuristicHeuristicState()
        }
        self.default_state = InvalidState()

    def handle_request(self, type1, type2):
        players = {}
        state = self.states.get((type1, type2), self.default_state)
        return state.handle(type1, type2, players)