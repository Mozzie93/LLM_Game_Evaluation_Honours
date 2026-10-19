from abc import ABC, abstractmethod


class JustOneGuesser(ABC):

    def __init__(self):
        self.move_history = []

    def set_move_history(self, move_history):
        self.move_history = move_history

    def get_move_history(self):
        return self.move_history

    @abstractmethod
    def set_clues(self, clues):
        pass

    @abstractmethod
    def get_guess(self):
        pass


class HumanJustOneGuesser(JustOneGuesser):

    def __init__(self, name="Guesser"):
        super().__init__()
        self.name = name

    def set_clues(self, clues):
        self.clues = clues
        print("The clues are:", clues)

    def get_guess(self):
        print(f"\n{self.name} — clues: {self.clues}")
        guess = input("What is the target word? (or 'pass' to skip) >> ").strip()
        return guess
