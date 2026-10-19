from openai import OpenAI

openAI_api_key = "INSERT API KEY HERE"

# https://czechgames.com/files/rules/codenames-rules-en.pdf
# Codemaster = Spymaster, Guesser = Field Operative
codenames_rules = """
Codenames is a word-based game of language understanding and communication.
Players are split into two teams (red and blue), with each team consisting of a Codemaster and Guesser.
Setup:
At the start of the game, the board consists of 25 English words.
The Codemasters on each team has access to a hidden map that tells them the identity of all of the words (Red, Blue, Civilian or Assassin).
The Guessers on each team do not have access to this map, and so do not know the identity of any words.
Players need to work as a team to select their words as quickly as possible, while minimizing the number of incorrect guesses.
Turns:
At the start of each team's turn, the Codemaster supplies a clue and a number (the number of words related to that clue).
The clue must:
- Be semantically related to the words the Codemaster wants their Guesser to guess.
- Be a single English word.
- NOT be derived from or derive one of the words on the board.
The Guesser then selects from the remaining words on he board, based on the which words are most associated with the Codemaster's clue.
The identity of the selected word is then revealed to all players.
If the Guesser selected a word that is their team's colour, then they may get to pick another word.
The Guesser must always make at least one guess each turn, and can guess up to one word more than the number provided in the Codemaster's clue.
If a Guesser selects a word that is not their team's colour, their turn ends.
The Guesser can choose to stop selecting words (ending their turn) any time after the first guess.
Ending:
Play proceeds, passing back and forth, until one of three outcomes is achieved:
All of the words of your team's colour have been selected -- you win
All of the words of the other team's colour have been selected -- you lose
You select the assassin tile -- you lose

"""
just_one_rules = """
Just One is a cooperative word-association game focused on generating useful clues while avoiding duplicated information.

Players work together toward a shared objective.
Each round involves two primary functional roles:
- Guesser: attempts to identify the hidden target word.
- Clue-Givers: independently generate clues to help the Guesser identify the target.

Roles rotate between rounds so different players take turns acting as the Guesser.

Setup:
At the start of each round:
- One player becomes the Guesser.
- A hidden target word is selected.
- All Clue-Givers can see the target word.
- The Guesser cannot see the target word.

Objective:
The Clue-Givers must help the Guesser identify the hidden word using indirect semantic clues.

Turns:
During a round:

1. Clue Generation Phase:
- Each Clue-Giver independently writes a single clue intended to help the Guesser identify the target word.
- Clues should ideally be:
  - Semantically related to the target.
  - Informative and distinctive.
  - Likely to survive duplication removal.

Clue restrictions:
- A clue should generally consist of a single word.
- Clues should not directly contain the target word.
- Clues should not be trivial variations, translations, abbreviations, or spellings of the target word.
- Clue-Givers may not coordinate while writing clues.

2. Duplicate Removal Phase:
- All clues are revealed to the Clue-Givers.
- Any duplicated clues are removed before the Guesser sees them.
- Near-identical clues may also be removed depending on implementation rules.

Examples of removable duplicates:
- Exact matches.
- Simple pluralization variants.
- Extremely similar derivations.

3. Guessing Phase:
- The remaining valid clues are shown to the Guesser.
- The Guesser makes a single attempt to identify the hidden target word.

Scoring:
- The team typically gains points for each correctly guessed target word.
- Incorrect guesses or skipped rounds may reduce the team's final score.

Ending:
Play proceeds for a fixed number of rounds.
The team receives a final score based on the number of successful guesses.

Information Dynamics:
- Clue-Givers must balance informativeness against collision risk.
- Highly obvious clues are more likely to be duplicated and removed.
- Highly obscure clues may survive duplication but fail to help the Guesser.

Strategy:
Successful play requires:
- Modeling how other Clue-Givers think.
- Predicting likely clue overlap.
- Generating semantically informative but distinctive associations.
- Understanding how the Guesser interprets partial semantic information.

Core Challenge:
The central challenge of Just One is cooperative constrained communication:
- Clue-Givers independently attempt to provide useful information.
- But overlapping information is discarded.
- The Guesser must infer the hidden concept from incomplete and non-coordinated semantic signals.

"""

decrypto_rules = """
Decrypto is a team-based communication and codebreaking game focused on interpreting encrypted clues and predicting opponent reasoning.

Players are split into two teams.
Each team has access to:
- Four secret code words visible only to their own team.
- A communication history of previous clues and guesses.

The game involves three distinct functional roles:
- Encryptor: generates clues for their team.
- Decryptor: interprets clues to recover the intended code sequence.
- Interceptor: attempts to infer the opposing team's code sequence from observed clues.

These roles may rotate between players or be handled collectively depending on the implementation.

Setup:
At the start of the game:
- Each team receives four secret code words, indexed from 1 to 4.
- Teams can only see their own code words.
- A sequence of hidden numbers (e.g. 2-4-1) is generated each round for each team.
- Only the Encryptor for that team sees the current sequence.

Objective:
Your team must:
- Successfully communicate your own code sequences to your Decryptors.
- Prevent the opposing Interceptors from correctly inferring your sequences.

Turns:
During a team's turn:

1. Encryptor Phase:
- The Encryptor sees the secret number sequence.
- For each number in the sequence, the Encryptor gives a clue related to the corresponding secret word.
- Clues should help teammates identify the intended code word position.
- Clues may be single words or short phrases depending on the implementation.
- Clues should avoid directly repeating or trivially modifying the secret code words.
- Encryptors must NEVER repeat a clue that was used in any previous round; every clue must be fresh and unique across the entire game.

Example:
If the team's secret words are:
1 = Moon
2 = Forest
3 = Glass
4 = River

And the sequence is 2-4-1

The Encryptor might say:
"Trees / Water / Night"

2. Decryptor Phase:
- The team's Decryptors observe the clues.
- They attempt to reconstruct the intended number sequence.
- A correct reconstruction means the team successfully transmitted the message.

3. Interceptor Phase:
- The opposing team acts as Interceptors.
- They observe the same clues but do NOT know the secret words.
- Using clue history and pattern inference, they attempt to predict the hidden number sequence.
- Correct interceptions award interception progress or points.

Information Structure:
- Teams accumulate clue history over multiple rounds.
- Because clues for the same secret words recur over time, opponents can gradually infer semantic patterns.
- Successful play requires balancing clarity for teammates against ambiguity for opponents.

Failure Conditions:
A team may receive penalties if:
- Their Decryptors fail to identify their own sequence.
- The opposing Interceptors correctly infer their sequence.

Ending:
Play proceeds until one of the following occurs:
- A team accumulates enough successful interceptions to win.
- A team accumulates too many communication failures and loses.
- A predefined number of rounds is completed.

Strategy:
Successful play requires:
- Consistent internal semantic associations.
- Long-term clue planning.
- Modeling teammate interpretation.
- Anticipating how opponents update beliefs from repeated observations.
- Managing information leakage across rounds.

Core Challenge:
The central tension of Decrypto is asymmetric language interpretation:
- Encryptors must communicate enough information for allied Decryptors.
- While simultaneously minimizing information available to enemy Interceptors.

"""
wavelength_rules = """
Wavelength is a communication and interpretation game based on estimating positions along conceptual spectrums.

Players are split into two teams.
Each team takes turns with one player acting as the Psychic for that round.

Setup:
At the start of each round:
- A spectrum is revealed with two opposite concepts at each end (e.g. Hot ↔ Cold, Chaotic ↔ Organized).
- A hidden target position is randomly selected somewhere along the spectrum.
- Only the Psychic can see the target position.

Objective:
The Psychic must communicate information that helps their team identify the hidden target position as accurately as possible.

Turns:
During their turn:
- The Psychic gives a single clue.
- The clue should indicate something that belongs at or near the hidden target position on the spectrum.
- The clue can be any phrase, concept, person, object, event, etc.
- The Psychic may not directly describe the numerical position or explicitly reference the spectrum mechanics.

The Guessers on the Psychic's team:
- Discuss the clue together.
- Rotate a dial to indicate where they believe the hidden target lies on the spectrum.

After the guess is locked in:
- The hidden target is revealed.
- Points are awarded based on how closely the team's guess overlaps the target area.

Optional Competitive Rules:
- The opposing team may make a bonus guess about whether the true target is to the left or right of the active team's final guess.
- Bonus points may be awarded for correct opponent guesses.

Ending:
Play proceeds for a fixed number of rounds or until a target score is reached.
The team with the highest score at the end of the game wins.

Strategy:
Successful play requires:
- Shared cultural knowledge and associations.
- Understanding how teammates interpret concepts.
- Giving clues that are specific enough to guide teammates, but broad enough to indicate position on a continuous scale.

"""

class GPT:

    def __init__(self, system_prompt, version):
        super().__init__()
        self.model_version = version
        self.client = OpenAI(api_key=openAI_api_key)
        self.conversation_history = [{"role": "system", "content": system_prompt}]

    def talk_to_ai(self, prompt):
        self.conversation_history.append({"role": "user", "content": prompt})
        response = self.client.chat.completions.create(
            messages=self.conversation_history,
            model=self.model_version,
            max_completion_tokens=512
        ).choices[0].message.content
        self.conversation_history.append({"role": "assistant", "content": response})
        return response
