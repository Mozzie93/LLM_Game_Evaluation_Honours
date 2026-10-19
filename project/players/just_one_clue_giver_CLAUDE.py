from claude_manager import just_one_rules, CLAUDE
from players.just_one_clue_giver import JustOneClueGiver


class AIJustOneClueGiver(JustOneClueGiver):

    def __init__(self, name="ClueGiver", version="claude-opus-5"):
        super().__init__()
        self.name = name
        system_prompt = just_one_rules + "You are playing Just One as a Clue-Giver. "
        self.manager = CLAUDE(system_prompt=system_prompt, version=version)

    def set_target_word(self, word):
        self.target_word = word

    def get_clue(self):
        invalid_timer = 0
        prompt = ""
        while True:
            prompt += (
                f"The mystery word is: {self.target_word}\n"
                "Give a single-word clue that will help the Guesser identify this word.\n"
                "Do not use the word itself, trivial variations, or direct translations.\n"
                "Try to be creative and avoid giving the same clue as other Clue-Givers.\n"
                "Respond with only the single-word clue, no additional text. "
            )
            response = self.manager.talk_to_ai(prompt).strip()
            print(f"  {self.name} clue: {response}")
            clue = response.split()[0].strip(".,!?\"';:") if response.split() else "default"
            if invalid_timer > 10:
                print(f"  Too many invalid attempts, using: {clue}")
                return clue
            invalid_timer += 1
            return clue
