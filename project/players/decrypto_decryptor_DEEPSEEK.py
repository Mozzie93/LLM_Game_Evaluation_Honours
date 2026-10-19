import re

from deepseek_manager import decrypto_rules, DEEPSEEK
from players.decrypto_decryptor import DecryptoDecryptor


class AIDecryptoDecryptor(DecryptoDecryptor):

    def __init__(self, team="Blue", version="deepseek-chat"):
        super().__init__()
        self.team = team
        system_prompt = (
            decrypto_rules
            + "You are playing the game Decrypto as the "
            + team
            + " team's INTERCEPTOR. "
            + "Your ONLY role is to intercept the opposing team's transmissions. "
            + "You do NOT decrypt for your own team. "
            + "You will observe the opposing team's clues and try to guess their hidden number sequence. "
            + "IMPORTANT: Each hidden number sequence always consists of 3 DISTINCT numbers chosen from 1-4 "
            + "(e.g. 2-4-1, never 2-2-3). All three numbers in a sequence are always different."
        )
        self.manager = DEEPSEEK(system_prompt=system_prompt, version=version)

    def set_code_words(self, code_words):
        self.code_words = code_words

    def set_clues(self, clues):
        self.clues = clues
        print("The clues are:", clues)

    def _parse_guess(self, response):
        if not response:
            return None
        match = re.fullmatch(r"\s*([1-4])\s*-\s*([1-4])\s*-\s*([1-4])\s*", response)
        if not match:
            return None
        guess = [int(match.group(i)) for i in range(1, 4)]
        if len(set(guess)) != 3:
            return None
        return guess

    def get_guess(self):
        invalid_timer = 0
        prompt = (
            f"Your team's secret code words (indexed 1-4) are:\n"
            f"1: {self.code_words[0]}\n"
            f"2: {self.code_words[1]}\n"
            f"3: {self.code_words[2]}\n"
            f"4: {self.code_words[3]}\n"
            f"The Encryptor's clues are: "
            f"{self.clues[0]} / {self.clues[1]} / {self.clues[2]}\n"
            "For each clue, determine which secret code word (1-4) it refers to.\n"
            "IMPORTANT: All 3 numbers must be DIFFERENT (no duplicates).\n"
            "Do NOT provide any reasoning, working out, or explanation.\n"
            "Reply with ONLY the 3 unique numbers separated by '-', nothing else.\n"
            "Example format: 2-4-1\n"
        )
        while True:
            response = self.manager.talk_to_ai(prompt).strip()
            print(response)
            guess = self._parse_guess(response)
            if guess is not None:
                return guess
            if invalid_timer > 10:
                print("Too many invalid attempts, defaulting to 1-2-3")
                return [1, 2, 3]
            invalid_timer += 1
            prompt = "That response was invalid. Reply with ONLY the 3 different numbers from 1-4 in the exact format X-Y-Z (e.g. 2-4-1). No explanations, no working out, no extra text."

    def get_interception_guess(self):
        invalid_timer = 0
        current_round = len(self.move_history) + 1
        clue_history = ""
        if self.move_history:
            clue_history = "Past clue history from the opposing team:\n"
            for entry in self.move_history:
                rnd = entry.get("round", "?")
                clues = entry.get("clues", "?")
                clue_history += f"  Round {rnd}: clues = {clues}\n"

        prompt = (
            f"You are the {self.team} team's Interceptor.\n"
            f"Current round: {current_round}\n\n"
            f"{clue_history}\n"
            f"The opposing team's Encryptor gave these clues this round:\n"
            f"  Clue 1: {self.clues[0]}\n"
            f"  Clue 2: {self.clues[1]}\n"
            f"  Clue 3: {self.clues[2]}\n\n"
            "You do NOT know their secret code words.\n"
            "Based on the clues and past history, infer the hidden number sequence.\n"
            "Each number (1-4) corresponds to one of their secret code words.\n"
            "CRITICAL: The sequence always uses 3 DISTINCT numbers from 1-4.\n"
            "All three numbers must be different — never repeat a number (e.g. 2-2-3 is INVALID).\n"
            "Do NOT provide any reasoning, working out, or explanation.\n"
            "Reply with ONLY the 3 different numbers separated by '-', nothing else.\n"
            "Example format: 2-4-1\n"
        )
        while True:
            response = self.manager.talk_to_ai(prompt).strip()
            print(response)
            guess = self._parse_guess(response)
            if guess is not None:
                return guess
            if invalid_timer > 10:
                print("Too many invalid attempts, defaulting to 1-2-3")
                return [1, 2, 3]
            invalid_timer += 1
            prompt = "That response was invalid. Reply with ONLY the 3 different numbers from 1-4 in the exact format X-Y-Z (e.g. 2-4-1). No explanations, no working out, no extra text."
