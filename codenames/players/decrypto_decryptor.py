from abc import ABC, abstractmethod


class DecryptoDecryptor(ABC):

    def __init__(self):
        self.move_history = []

    def set_move_history(self, move_history):
        self.move_history = move_history

    def get_move_history(self):
        return self.move_history

    @abstractmethod
    def set_code_words(self, code_words):
        pass

    @abstractmethod
    def set_clues(self, clues):
        pass

    @abstractmethod
    def get_guess(self):
        pass

    @abstractmethod
    def get_interception_guess(self):
        pass


class HumanDecryptoDecryptor(DecryptoDecryptor):

    def __init__(self, team="Red"):
        super().__init__()
        self.team = team

    def set_code_words(self, code_words):
        self.code_words = code_words

    def set_clues(self, clues):
        self.clues = clues
        print("The clues are:", clues)

    def get_guess(self):
        print(f"\nYour team's code words:")
        for i, w in enumerate(self.code_words, 1):
            print(f"  {i}: {w}")
        print(f"Encryptor's clues: {self.clues[0]} / {self.clues[1]} / {self.clues[2]}")
        guess_input = input("Enter the sequence (3 numbers 1-4 separated by '-') >> ")
        parts = guess_input.replace(",", "-").split("-")
        guess = [int(p.strip()) for p in parts if p.strip()]
        while len(guess) != 3 or not all(1 <= g <= 4 for g in guess):
            guess_input = input("Invalid. Enter 3 numbers 1-4 separated by '-' >> ")
            parts = guess_input.replace(",", "-").split("-")
            guess = [int(p.strip()) for p in parts if p.strip()]
        return guess

    def get_interception_guess(self):
        print(f"\nOpponent's clues: {self.clues[0]} / {self.clues[1]} / {self.clues[2]}")
        print("(You don't know their code words)")
        guess_input = input("Intercept the sequence (3 numbers 1-4 separated by '-') >> ")
        parts = guess_input.replace(",", "-").split("-")
        guess = [int(p.strip()) for p in parts if p.strip()]
        while len(guess) != 3 or not all(1 <= g <= 4 for g in guess):
            guess_input = input("Invalid. Enter 3 numbers 1-4 separated by '-' >> ")
            parts = guess_input.replace(",", "-").split("-")
            guess = [int(p.strip()) for p in parts if p.strip()]
        return guess
