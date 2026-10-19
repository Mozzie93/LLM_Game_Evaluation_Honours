from abc import ABC, abstractmethod


class WavelengthClueGiver(ABC):
    """Wavelength abstract class that mimics the cluegiver in the wavelength game"""

    def __init__(self):
        """Set up word list and handle pretrained vectors"""
        self.move_history = []
        pass

    def set_move_history(self, move_history):
        """Called periodically by the Game to update the current move history"""
        self.move_history = move_history

    def get_move_history(self):
        """Called to access the current move history"""
        return self.move_history

    @abstractmethod
    def set_game_state(self, scale, number):
        """Set the current spectrum and target number for this round"""
        pass

    @abstractmethod
    def get_clue(self):
        """Return a clue word or phrase that hints at the target position"""
        pass


class HumanCodemaster(WavelengthClueGiver):

    def __init__(self, team="Red"):
        super().__init__()
        self.team = team

    def set_game_state(self, scale, number):
        self.scale = scale
        self.number = number

    def get_clue(self):
        print(f"Spectrum: {self.scale[0]} \u2194 {self.scale[1]}")
        print(f"Target: {self.number}")
        clue_input = input("Input Clue:\nPlease enter a Word or Phrase >> ")
        return clue_input
