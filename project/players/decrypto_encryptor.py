from abc import ABC, abstractmethod


class DecryptoEncryptor(ABC):

    def __init__(self):
        self.move_history = []

    def set_move_history(self, move_history):
        self.move_history = move_history

    def get_move_history(self):
        return self.move_history

    @abstractmethod
    def set_game_state(self, code_words, sequence):
        pass

    @abstractmethod
    def get_clue(self):
        pass


class HumanDecryptoEncryptor(DecryptoEncryptor):

    def __init__(self, team="Red"):
        super().__init__()
        self.team = team

    def set_game_state(self, code_words, sequence):
        self.code_words = code_words
        self.sequence = sequence

    def get_clue(self):
        print(f"\nYour team's code words:")
        for i, w in enumerate(self.code_words, 1):
            print(f"  {i}: {w}")
        print(f"Sequence to transmit: {self.sequence[0]}-{self.sequence[1]}-{self.sequence[2]}")
        clue_input = input("Enter 3 clues separated by '/' >> ")
        clues = [c.strip() for c in clue_input.replace(",", "/").split("/") if c.strip()]
        while len(clues) < 3:
            clues.append("")
        return clues[:3]
