# DeepSeek uses an OpenAI-compatible API.
from openai import OpenAI

# >>> PASTE YOUR DEEPSEEK API KEY HERE <<<
DEEPSEEK_API_KEY = "INSERT API KEY HERE"

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


class DEEPSEEK:
    """Client for DeepSeek's OpenAI-compatible chat API."""

    def __init__(self, system_prompt, version="deepseek-chat"):
        super().__init__()
        self.model_version = version
        self.client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")
        self.conversation_history = [{"role": "system", "content": system_prompt}]

    def talk_to_ai(self, prompt):
        self.conversation_history.append({"role": "user", "content": prompt})
        response = self.client.chat.completions.create(
            messages=self.conversation_history,
            model=self.model_version,
            max_tokens=512
        ).choices[0].message.content
        if response is None:
            response = ""
        self.conversation_history.append({"role": "assistant", "content": response})
        return response