import re

# Paste your log results between the triple quotes below:
log_data = """
ROUNDS:3 R:47 B:0 CLUE_GIVER_R:AIWavelengthClueGiver GUESSER_R:AIWavelengthGuesser CLUE_GIVER_B:AIWavelengthClueGiver GUESSER_B:AIWavelengthGuesser SEED:0 WINNER:R
ROUNDS:3 R:60 B:0 CLUE_GIVER_R:AIWavelengthClueGiver GUESSER_R:AIWavelengthGuesser CLUE_GIVER_B:AIWavelengthClueGiver GUESSER_B:AIWavelengthGuesser SEED:1 WINNER:R
ROUNDS:3 R:31 B:0 CLUE_GIVER_R:AIWavelengthClueGiver GUESSER_R:AIWavelengthGuesser CLUE_GIVER_B:AIWavelengthClueGiver GUESSER_B:AIWavelengthGuesser SEED:2 WINNER:R
ROUNDS:3 R:39 B:0 CLUE_GIVER_R:AIWavelengthClueGiver GUESSER_R:AIWavelengthGuesser CLUE_GIVER_B:AIWavelengthClueGiver GUESSER_B:AIWavelengthGuesser SEED:3 WINNER:R
ROUNDS:3 R:28 B:0 CLUE_GIVER_R:AIWavelengthClueGiver GUESSER_R:AIWavelengthGuesser CLUE_GIVER_B:AIWavelengthClueGiver GUESSER_B:AIWavelengthGuesser SEED:4 WINNER:R
ROUNDS:3 R:42 B:0 CLUE_GIVER_R:AIWavelengthClueGiver GUESSER_R:AIWavelengthGuesser CLUE_GIVER_B:AIWavelengthClueGiver GUESSER_B:AIWavelengthGuesser SEED:5 WINNER:R
ROUNDS:3 R:117 B:0 CLUE_GIVER_R:AIWavelengthClueGiver GUESSER_R:AIWavelengthGuesser CLUE_GIVER_B:AIWavelengthClueGiver GUESSER_B:AIWavelengthGuesser SEED:6 WINNER:R
ROUNDS:3 R:96 B:0 CLUE_GIVER_R:AIWavelengthClueGiver GUESSER_R:AIWavelengthGuesser CLUE_GIVER_B:AIWavelengthClueGiver GUESSER_B:AIWavelengthGuesser SEED:7 WINNER:R
ROUNDS:3 R:67 B:0 CLUE_GIVER_R:AIWavelengthClueGiver GUESSER_R:AIWavelengthGuesser CLUE_GIVER_B:AIWavelengthClueGiver GUESSER_B:AIWavelengthGuesser SEED:8 WINNER:R
ROUNDS:3 R:30 B:0 CLUE_GIVER_R:AIWavelengthClueGiver GUESSER_R:AIWavelengthGuesser CLUE_GIVER_B:AIWavelengthClueGiver GUESSER_B:AIWavelengthGuesser SEED:9 WINNER:R
ROUNDS:3 R:26 B:0 CLUE_GIVER_R:AIWavelengthClueGiver GUESSER_R:AIWavelengthGuesser CLUE_GIVER_B:AIWavelengthClueGiver GUESSER_B:AIWavelengthGuesser SEED:10 WINNER:R
ROUNDS:3 R:26 B:0 CLUE_GIVER_R:AIWavelengthClueGiver GUESSER_R:AIWavelengthGuesser CLUE_GIVER_B:AIWavelengthClueGiver GUESSER_B:AIWavelengthGuesser SEED:11 WINNER:R
ROUNDS:3 R:20 B:0 CLUE_GIVER_R:AIWavelengthClueGiver GUESSER_R:AIWavelengthGuesser CLUE_GIVER_B:AIWavelengthClueGiver GUESSER_B:AIWavelengthGuesser SEED:12 WINNER:R
ROUNDS:3 R:23 B:0 CLUE_GIVER_R:AIWavelengthClueGiver GUESSER_R:AIWavelengthGuesser CLUE_GIVER_B:AIWavelengthClueGiver GUESSER_B:AIWavelengthGuesser SEED:13 WINNER:R
ROUNDS:3 R:28 B:0 CLUE_GIVER_R:AIWavelengthClueGiver GUESSER_R:AIWavelengthGuesser CLUE_GIVER_B:AIWavelengthClueGiver GUESSER_B:AIWavelengthGuesser SEED:14 WINNER:R
ROUNDS:3 R:84 B:0 CLUE_GIVER_R:AIWavelengthClueGiver GUESSER_R:AIWavelengthGuesser CLUE_GIVER_B:AIWavelengthClueGiver GUESSER_B:AIWavelengthGuesser SEED:15 WINNER:R
ROUNDS:3 R:57 B:0 CLUE_GIVER_R:AIWavelengthClueGiver GUESSER_R:AIWavelengthGuesser CLUE_GIVER_B:AIWavelengthClueGiver GUESSER_B:AIWavelengthGuesser SEED:16 WINNER:R
ROUNDS:3 R:36 B:0 CLUE_GIVER_R:AIWavelengthClueGiver GUESSER_R:AIWavelengthGuesser CLUE_GIVER_B:AIWavelengthClueGiver GUESSER_B:AIWavelengthGuesser SEED:17 WINNER:R
ROUNDS:3 R:51 B:0 CLUE_GIVER_R:AIWavelengthClueGiver GUESSER_R:AIWavelengthGuesser CLUE_GIVER_B:AIWavelengthClueGiver GUESSER_B:AIWavelengthGuesser SEED:18 WINNER:R
ROUNDS:3 R:7 B:0 CLUE_GIVER_R:AIWavelengthClueGiver GUESSER_R:AIWavelengthGuesser CLUE_GIVER_B:AIWavelengthClueGiver GUESSER_B:AIWavelengthGuesser SEED:19 WINNER:R
ROUNDS:3 R:149 B:0 CLUE_GIVER_R:AIWavelengthClueGiver GUESSER_R:AIWavelengthGuesser CLUE_GIVER_B:AIWavelengthClueGiver GUESSER_B:AIWavelengthGuesser SEED:20 WINNER:R
ROUNDS:3 R:53 B:0 CLUE_GIVER_R:AIWavelengthClueGiver GUESSER_R:AIWavelengthGuesser CLUE_GIVER_B:AIWavelengthClueGiver GUESSER_B:AIWavelengthGuesser SEED:21 WINNER:R
ROUNDS:3 R:38 B:0 CLUE_GIVER_R:AIWavelengthClueGiver GUESSER_R:AIWavelengthGuesser CLUE_GIVER_B:AIWavelengthClueGiver GUESSER_B:AIWavelengthGuesser SEED:22 WINNER:R
ROUNDS:3 R:43 B:0 CLUE_GIVER_R:AIWavelengthClueGiver GUESSER_R:AIWavelengthGuesser CLUE_GIVER_B:AIWavelengthClueGiver GUESSER_B:AIWavelengthGuesser SEED:23 WINNER:R
ROUNDS:3 R:144 B:0 CLUE_GIVER_R:AIWavelengthClueGiver GUESSER_R:AIWavelengthGuesser CLUE_GIVER_B:AIWavelengthClueGiver GUESSER_B:AIWavelengthGuesser SEED:24 WINNER:R
ROUNDS:3 R:34 B:0 CLUE_GIVER_R:AIWavelengthClueGiver GUESSER_R:AIWavelengthGuesser CLUE_GIVER_B:AIWavelengthClueGiver GUESSER_B:AIWavelengthGuesser SEED:25 WINNER:R
ROUNDS:3 R:35 B:0 CLUE_GIVER_R:AIWavelengthClueGiver GUESSER_R:AIWavelengthGuesser CLUE_GIVER_B:AIWavelengthClueGiver GUESSER_B:AIWavelengthGuesser SEED:26 WINNER:R
ROUNDS:3 R:86 B:0 CLUE_GIVER_R:AIWavelengthClueGiver GUESSER_R:AIWavelengthGuesser CLUE_GIVER_B:AIWavelengthClueGiver GUESSER_B:AIWavelengthGuesser SEED:27 WINNER:R
ROUNDS:3 R:20 B:0 CLUE_GIVER_R:AIWavelengthClueGiver GUESSER_R:AIWavelengthGuesser CLUE_GIVER_B:AIWavelengthClueGiver GUESSER_B:AIWavelengthGuesser SEED:28 WINNER:R
ROUNDS:3 R:33 B:0 CLUE_GIVER_R:AIWavelengthClueGiver GUESSER_R:AIWavelengthGuesser CLUE_GIVER_B:AIWavelengthClueGiver GUESSER_B:AIWavelengthGuesser SEED:29 WINNER:R
"""

def extract_r_values(raw_text: str) -> None:
    # Matches the numeric score specifically following "R:" (ignoring WINNER:R or other R references)
    r_values = re.findall(r'\bR:(\d+)', raw_text)
    
    if not r_values:
        print("No 'R:' values found.")
        return

    # Print as a clean single column for Excel
    print("\n".join(r_values))

if __name__ == "__main__":
    extract_r_values(log_data)