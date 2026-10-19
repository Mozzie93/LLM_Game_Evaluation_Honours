from gpt_manager import wavelength_rules, GPT
from players.wavelength_guesser import WavelengthGuesser


class AIWavelengthGuesser(WavelengthGuesser):

    def __init__(self, team="Red", version="gpt-5.6-terra"):
        super().__init__()
        self.team = team
        system_prompt = wavelength_rules + "You are playing the game Wavelength as the " + team + " Guesser. "
        self.manager = GPT(system_prompt=system_prompt, version=version)

    def set_scale(self, scale):
        self.scale = scale

    def set_clue(self, clue):
        self.clue = clue
        print("The clue is:", clue)

    def get_guess(self):
        invalid_timer = 0
        guess = None
        prompt = ""
        while guess is None:
            prompt += (
                f"The spectrum is: {self.scale[0]} \u2194 {self.scale[1]}.\n"
                f"The Psychic's clue is: {self.clue}.\n"
                "Decide where on the spectrum (1-100) the hidden target is located.\n"
                "1 means closest to the left concept, 100 means closest to the right concept.\n"
                "Respond with only a number between 1 and 100, no additional text. "
            )
            response = self.manager.talk_to_ai(prompt)
            print(response)
            try:
                guess = int(response.strip())
                if guess < 1 or guess > 100:
                    guess = None
            except ValueError:
                pass
            if invalid_timer > 10:
                print("Too many invalid attempts, defaulting to 50")
                guess = 50
            invalid_timer += 1
        return guess
