from gemini_manager import decrypto_rules, GEMINI
from players.decrypto_encryptor import DecryptoEncryptor


class AIDecryptoEncryptor(DecryptoEncryptor):

    def __init__(self, team="Red", version="gemini-3.5-flash-lite"):
        super().__init__()
        self.team = team
        self.blocked_clues = set()
        system_prompt = decrypto_rules + "You are playing the game Decrypto as the " + team + " Encryptor. "
        self.manager = GEMINI(system_prompt=system_prompt, version=version)

    def set_game_state(self, code_words, sequence):
        self.code_words = code_words
        self.sequence = sequence

    def block_clues(self, clues):
        self.blocked_clues.update(c.strip().lower() for c in clues)

    def _already_used_clues(self):
        used = set(self.blocked_clues)
        for entry in self.move_history:
            for clue in entry.get("clues", []):
                used.add(str(clue).strip().lower())
        return used

    def _previous_clues_text(self):
        used = sorted(self._already_used_clues())
        if not used:
            return "There are no previously used clues yet.\n"
        return ("Clues already used in previous rounds (you must NOT reuse any of these):\n"
                + ", ".join(used) + "\n")

    def get_clue(self):
        invalid_timer = 0
        prompt = ""
        while True:
            used_clues = self._already_used_clues()
            prompt += (
                f"Your team's secret code words (indexed 1-4) are:\n"
                f"1: {self.code_words[0]}\n"
                f"2: {self.code_words[1]}\n"
                f"3: {self.code_words[2]}\n"
                f"4: {self.code_words[3]}\n"
                f"The hidden sequence to transmit is: "
                f"{self.sequence[0]}-{self.sequence[1]}-{self.sequence[2]}\n"
                f"{self._previous_clues_text()}"
                "Provide exactly 3 clues, one for each number in the sequence, in order.\n"
                "Each clue should be semantically related to the corresponding secret word.\n"
                "Do not directly use or trivially modify the secret code words.\n"
                "IMPORTANT RULE: It is against the rules to repeat any clue that was used in a "
                "previous round. All 3 clues must be completely new and not appear in the list of "
                "already used clues, and they must all be different from each other.\n"
                "Respond with only the 3 clues separated by '/', no additional text.\n"
                "Example format: trees/water/night\n"
            )
            response = self.manager.talk_to_ai(prompt).strip()
            print(response)
            clues = [c.strip() for c in response.replace(",", "/").split("/") if c.strip()]
            if len(clues) >= 3:
                clues = clues[:3]
                repeated = [c for c in clues if c.strip().lower() in used_clues]
                if not repeated and len(set(c.lower() for c in clues)) == len(clues):
                    return clues
                self.block_clues(repeated)
                invalid_timer += 1
                print(f"  *** Encryptor repeated previously used clue(s): {repeated}. Re-prompting. ***")
                prompt = ("That was invalid because the following clues have already been used in this "
                          f"game: {repeated}. Provide exactly 3 brand-new clues separated by '/' that "
                          "have never been used before and are all different from each other. ")
                continue
            if invalid_timer > 10:
                print("Too many invalid attempts, splitting by spaces")
                clues = response.split()
                while len(clues) < 3:
                    clues.append("default")
                return clues[:3]
            invalid_timer += 1
            prompt = "That format was invalid. Provide exactly 3 clues separated by '/'. "
