from claude_manager import codenames_rules, CLAUDE
from players.guesser import Guesser
import random


class ClaudeGuesser(Guesser):
    def __init__(self, team="Red"):
        super().__init__()
        self.team = team
        self.num = 0
        self.guesses = 0
        system_prompt = codenames_rules + "You are playing the game Codenames as the " + team + " Guesser. "
        self.manager = CLAUDE(system_prompt=system_prompt, version="claude-haiku-4-5")

    def set_board(self, words):
        self.words = words

    def set_clue(self, clue, num):
        self.clue = clue
        self.num = num
        print("The clue is:", clue, num)
        li = [clue, num]
        return li

    def keep_guessing(self):
        invalid_timer = 0
        response = None
        # FIX 1: Move error state to a clean variable instead of accumulating into 'prompt'
        error_prefix = "" 
        guess_again = False
        
        while response is None and (self.guesses <= self.num or self.num == 0):
            # Construct a fresh prompt every loop iteration
            prompt = error_prefix
            prompt += "The remaining words are: " + str(self.get_remaining_options()) + ". "
            prompt += "The following is the Codemaster's clue: (" + str(self.clue) + ", " + str(self.num) + "). "
            prompt += "You have picked " + str(self.guesses) + " words this turn. "
            prompt += "Would you like to keep guessing? Answer only 'yes' or 'no'. "
            
            response = self.manager.talk_to_ai(prompt)
            
            if "yes" in response.lower():
                guess_again = True
            elif "no" in response.lower():
                guess_again = False
            elif invalid_timer > 10:
                guess_again = False
            else:
                response = None
                invalid_timer += 1
                # Update the error state for the next clean iteration
                error_prefix = "That was not a valid response, respond with only 'yes' or 'no'. "
                
        return guess_again

    def get_remaining_options(self):
        remaining_options = []
        for i in range(len(self.words)):
            if self.words[i][0] == '*':
                continue
            remaining_options.append(self.words[i])
        return remaining_options

    def get_answer(self):
        invalid_timer = 0
        guess = None
        # FIX 2: Prevent prompt duplication here too
        error_prefix = ""
        
        while guess is None:
            # Construct a fresh prompt every loop iteration
            prompt = error_prefix
            prompt += "The remaining words are: " + str(self.get_remaining_options()) + ". "
            prompt += "The following is the Codemaster's clue: (" + str(self.clue) + ", " + str(self.num) + "). "
            prompt += "Select one of the remaining words that is most associated with this clue. "
            prompt += "You must select one of the remaining words and provide no additional text. "
            
            print("\n\n" + prompt + "\n\n")
            response = self.manager.talk_to_ai(prompt)
            print(response)
            response = response.upper().strip()
            
            if response in self.words:
                guess = response
            elif response.split(" ")[0].strip() in self.words:
                guess = response.split(" ")[0].strip()
            elif response.split('"')[1:2] and response.split('"')[1] in self.words: # Added safety check
                guess = response.split('"')[1]
            elif response.split("'")[1:2] and response.split("'")[1] in self.words: # Added safety check
                guess = response.split("'")[1]
            elif invalid_timer > 10:
                print("You have made too many invalid guesses, selecting random remaining word")
                guess = random.choice(self.get_remaining_options())
            else:
                print("Warning! Invalid guess: " + response)
                error_prefix = "That was not a valid word. "
                invalid_timer += 1
                
        self.guesses += 1
        return guess

