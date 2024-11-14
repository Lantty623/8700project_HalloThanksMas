import pickle

class Memento:
    def __init__(self, state):
        self.state = state

    def get_state(self):
        return self.state

class Caretaker:
    def __init__(self):
        self.mementos = []

    def save_state(self, memento):
        self.mementos.append(memento)
        with open('game_state.pkl', 'wb') as f:
            pickle.dump(self.mementos, f)

    def load_state(self):
        try:
            with open('game_state.pkl', 'rb') as f:
                self.mementos = pickle.load(f)
            return self.mementos[-1].get_state()
        except (FileNotFoundError, IndexError):
            return None