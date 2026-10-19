import re

# Paste your experiment results between the triple quotes below:
log_data = """
time=19.03, turns=10, name=Claude-Claude, winner=R
time=16.30, turns=9, name=Claude-Claude, winner=R
time=18.97, turns=10, name=Claude-Claude, winner=R
time=15.32, turns=8, name=Claude-Claude, winner=R
time=17.13, turns=10, name=Claude-Claude, winner=R
time=13.07, turns=8, name=Claude-Claude, winner=R
time=17.94, turns=11, name=Claude-Claude, winner=R
time=14.94, turns=9, name=Claude-Claude, winner=R
time=17.26, turns=9, name=Claude-Claude, winner=R
time=15.32, turns=8, name=Claude-Claude, winner=R
time=16.55, turns=10, name=Claude-Claude, winner=R
time=1.58, turns=1, name=Claude-Claude, winner=B
time=14.18, turns=8, name=Claude-Claude, winner=B
time=16.44, turns=10, name=Claude-Claude, winner=R
time=17.77, turns=10, name=Claude-Claude, winner=R
time=8.20, turns=1, name=Claude-Claude, winner=B
time=14.81, turns=8, name=Claude-Claude, winner=R
time=14.99, turns=8, name=Claude-Claude, winner=R
time=16.21, turns=9, name=Claude-Claude, winner=R
time=19.23, turns=10, name=Claude-Claude, winner=R
time=16.11, turns=9, name=Claude-Claude, winner=R
time=15.81, turns=10, name=Claude-Claude, winner=R
time=21.59, turns=11, name=Claude-Claude, winner=R
time=19.68, turns=12, name=Claude-Claude, winner=R
time=16.47, turns=9, name=Claude-Claude, winner=R
time=15.74, turns=9, name=Claude-Claude, winner=R
time=18.01, turns=10, name=Claude-Claude, winner=R
time=17.94, turns=11, name=Claude-Claude, winner=R
time=13.38, turns=8, name=Claude-Claude, winner=R
time=14.79, turns=8, name=Claude-Claude, winner=R
"""

def extract_turns(raw_text: str) -> None:
    # Find all digits following "turns="
    turns = re.findall(r'turns=(\d+)', raw_text)
    
    if not turns:
        print("No 'turns=' entries found.")
        return

    # Output the column formatted for Excel
    print("\n".join(turns))

if __name__ == "__main__":
    extract_turns(log_data)