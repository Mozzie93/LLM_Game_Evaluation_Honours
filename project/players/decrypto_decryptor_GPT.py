from gpt_manager import decrypto_rules, GPT
from players.decrypto_decryptor import DecryptoDecryptor


class AIDecryptoDecryptor(DecryptoDecryptor):

    def __init__(self, team="Red", version="gpt-4o-2024-05-13"):
        super().__init__()
        self.team = team
        system_prompt = decrypto_rules + "You are playing the game Decrypto as the " + team + " Decryptor/Interceptor. "
        self.manager = GPT(system_prompt=system_prompt, version=version)

    def set_code_words(self, code_words):
        self.code_words = code_words

    def set_clues(self, clues):
        self.clues = clues
        print("The clues are:", clues)

    def get_guess(self):
        invalid_timer = 0
        prompt = ""
        while True:
            prompt += (
                f"Your team's secret code words (indexed 1-4) are:\n"
                f"1: {self.code_words[0]}\n"
                f"2: {self.code_words[1]}\n"
                f"3: {self.code_words[2]}\n"
                f"4: {self.code_words[3]}\n"
                f"The Encryptor's clues are: "
                f"{self.clues[0]} / {self.clues[1]} / {self.clues[2]}\n"
                "For each clue, determine which secret code word (1-4) it refers to.\n"
                "Respond with only the 3 numbers separated by '-', no additional text.\n"
                "Example format: 2-4-1\n"
            )
            response = self.manager.talk_to_ai(prompt).strip()
            print(response)
            try:
                parts = response.replace(",", "-").split("-")
                guess = [int(p.strip()) for p in parts if p.strip()]
                if len(guess) == 3 and all(1 <= g <= 4 for g in guess):
                    return guess
            except ValueError:
                pass
            if invalid_timer > 10:
                print("Too many invalid attempts, defaulting to 1-1-1")
                return [1, 1, 1]
            invalid_timer += 1
            prompt = "That format was invalid. Provide exactly 3 numbers 1-4 separated by '-'. "

    def get_interception_guess(self):
        invalid_timer = 0
        prompt = ""
        while True:
            clue_history = ""
            if self.move_history:
                clue_history = "Past clue history:\n"
                for entry in self.move_history:
                    clue_history += f"  Round {entry.get('round', '?')}: {entry.get('clues', '?')}\n"

            prompt += (
                f"{clue_history}"
                f"The opposing team's Encryptor gave these clues:\n"
                f"{self.clues[0]} / {self.clues[1]} / {self.clues[2]}\n"
                "You do NOT know their secret code words.\n"
                "Based on the clues and past history, infer the hidden number sequence.\n"
                "Each number (1-4) corresponds to one of their secret code words.\n"
                "Respond with only the 3 numbers separated by '-', no additional text.\n"
                "Example format: 2-4-1\n"
            )
            response = self.manager.talk_to_ai(prompt).strip()
            print(response)
            try:
                parts = response.replace(",", "-").split("-")
                guess = [int(p.strip()) for p in parts if p.strip()]
                if len(guess) == 3 and all(1 <= g <= 4 for g in guess):
                    return guess
            except ValueError:
                pass
            if invalid_timer > 10:
                print("Too many invalid attempts, defaulting to 1-1-1")
                return [1, 1, 1]
            invalid_timer += 1
            prompt = "That format was invalid. Provide exactly 3 numbers 1-4 separated by '-'. "
