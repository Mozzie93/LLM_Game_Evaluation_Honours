from abc import ABC, abstractmethod


class WavelengthGuesser(ABC):
    """Wavelength abstract class that mimics the guesser in the wavelength game"""

    def __init__(self):
        self.move_history = []

    def set_move_history(self, move_history):
        self.move_history = move_history

    def get_move_history(self):
        return self.move_history

    @abstractmethod
    def set_scale(self, scale):
        """Set the current spectrum (concept pair) for this round"""
        pass

    @abstractmethod
    def set_clue(self, clue):
        """Set the clue from the clue giver"""
        pass

    @abstractmethod
    def get_guess(self):
        """Return the team's position guess as an integer (1-100)"""
        pass


class HumanGuesser(WavelengthGuesser):

    def __init__(self, team="Red"):
        super().__init__()
        self.team = team

    def set_scale(self, scale):
        self.scale = scale

    def set_clue(self, clue):
        self.clue = clue
        print("The clue is:", clue)

    def get_guess(self):
        while True:
            try:
                guess = int(input(
                    f"Spectrum: {self.scale[0]} \u2194 {self.scale[1]}\n"
                    f"Clue: {self.clue}\n"
                    "Enter your position guess (1-100) >> "
                ))
                if 1 <= guess <= 100:
                    return guess
                print("Please enter a number between 1 and 100.")
            except ValueError:
                print("Please enter a valid number.")
