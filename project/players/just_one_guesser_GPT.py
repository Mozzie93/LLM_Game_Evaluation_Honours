from gpt_manager import just_one_rules, GPT
from players.just_one_guesser import JustOneGuesser


class AIJustOneGuesser(JustOneGuesser):

    def __init__(self, name="Guesser", version="gpt-5.6-terra"):
        super().__init__()
        self.name = name
        system_prompt = just_one_rules + "You are playing Just One as the Guesser. "
        self.manager = GPT(system_prompt=system_prompt, version=version)

    def set_clues(self, clues):
        self.clues = clues
        print("The clues are:", clues)

    def get_guess(self):
        invalid_timer = 0
        prompt = ""
        while True:
            clue_list = " / ".join(self.clues)
            prompt += (
                f"The Clue-Givers' clues are: {clue_list}\n"
                "Based on these clues, what is the mystery word?\n"
                "If you cannot determine it, respond with 'pass'.\n"
                "Respond with only a single word (or 'pass'), no additional text. "
            )
            response = self.manager.talk_to_ai(prompt).strip()
            print(f"  Guesser says: {response}")
            guess = response.split()[0].strip(".,!?\"';:").lower()
            if guess in ("pass", "skip"):
                return "pass"
            if invalid_timer > 10:
                print("  Too many invalid attempts, guessing first word")
                return response.split()[0] if response.split() else "pass"
            invalid_timer += 1
            return guess
