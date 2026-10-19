from abc import ABC, abstractmethod


class JustOneClueGiver(ABC):

    def __init__(self):
        self.move_history = []

    def set_move_history(self, move_history):
        self.move_history = move_history

    def get_move_history(self):
        return self.move_history

    @abstractmethod
    def set_target_word(self, word):
        pass

    @abstractmethod
    def get_clue(self):
        pass


class HumanJustOneClueGiver(JustOneClueGiver):

    def __init__(self, name="Player"):
        super().__init__()
        self.name = name

    def set_target_word(self, word):
        self.target_word = word

    def get_clue(self):
        print(f"\n{self.name}'s turn — target word: {self.target_word}")
        clue = input("Enter your one-word clue >> ").strip()
        return clue
