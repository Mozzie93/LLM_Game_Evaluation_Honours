from claude_manager import wavelength_rules, CLAUDE
from players.wavelength_clue_giver import WavelengthClueGiver


class AIWavelengthClueGiver(WavelengthClueGiver):

    def __init__(self, team="Red", version="claude-haiku-4-5"):
        super().__init__()
        self.team = team
        system_prompt = wavelength_rules + "You are playing the game Wavelength as the " + team + " Psychic. "
        self.manager = CLAUDE(system_prompt=system_prompt, version=version)

    def set_game_state(self, scale, number):
        self.scale = scale
        self.number = number

    def get_clue(self):
        invalid_timer = 0
        clue = None
        prompt = ""
        while clue is None:
            prompt += (
                f"The spectrum is: {self.scale[0]} \u2194 {self.scale[1]}.\n"
                f"The hidden target position is at {self.number} on a scale of 1-100 "
                f"(1 = {self.scale[0]}, 100 = {self.scale[1]}).\n"
                "Provide a single clue word or short phrase that will help your team "
                "guess the target position.\n"
                "Do not use adjectives that directly describe the position.\n"
                "Respond with only the clue, no additional text. "
            )
            response = self.manager.talk_to_ai(prompt).strip()
            print(response)
            if invalid_timer > 10:
                print("Too many invalid attempts, using last response as clue")
                clue = response
            else:
                clue = response
            invalid_timer += 1

        return clue
