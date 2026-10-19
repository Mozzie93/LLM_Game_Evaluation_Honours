import random
import time
import json
import os
import sys
from enum import Enum


SPECTRUMS = [
    ("Hot", "Cold"),
    ("Light", "Dark"),
    ("Quiet", "Loud"),
    ("Fast", "Slow"),
    ("Happy", "Sad"),
    ("Love", "Hate"),
    ("Rich", "Poor"),
    ("Easy", "Hard"),
    ("Safe", "Dangerous"),
    ("Funny", "Serious"),
    ("Big", "Small"),
    ("Strong", "Weak"),
    ("Simple", "Complex"),
    ("Chaotic", "Orderly"),
    ("Cheap", "Expensive"),
    ("Soft", "Hard"),
    ("Smooth", "Rough"),
    ("Sweet", "Sour"),
    ("Thick", "Thin"),
    ("Sharp", "Dull"),
    ("Heavy", "Light"),
    ("Tall", "Short"),
    ("Wide", "Narrow"),
    ("Deep", "Shallow"),
    ("Bright", "Dim"),
    ("Full", "Empty"),
    ("Clean", "Dirty"),
    ("Young", "Old"),
    ("Early", "Late"),
    ("Open", "Closed"),
    ("Calm", "Excited"),
    ("Messy", "Tidy"),
    ("Rigid", "Flexible"),
    ("Rare", "Common"),
    ("Urban", "Rural"),
    ("Formal", "Casual"),
    ("Loose", "Tight"),
    ("Abstract", "Concrete"),
    ("Theoretical", "Practical"),
    ("Logical", "Emotional"),
    ("Bland", "Spicy"),
    ("Mild", "Intense"),
    ("Shy", "Outgoing"),
    ("Lazy", "Ambitious"),
    ("Gloomy", "Cheerful"),
    ("Cruel", "Kind"),
    ("Ugly", "Beautiful"),
    ("Tame", "Wild"),
    ("Dull", "Vibrant"),
    ("Stale", "Fresh"),
    ("Common", "Exotic"),
    ("Temporary", "Permanent"),
    ("Artificial", "Natural"),
    ("Subtle", "Obvious"),
    ("Vague", "Specific"),
    ("Passive", "Aggressive"),
    ("Fragile", "Durable"),
    ("Conventional", "Unconventional"),
    ("Timid", "Bold"),
    ("Earth", "Air"),
    ("Fire", "Water"),
    ("Peace", "War"),
    ("Order", "Chaos"),
    ("Life", "Death"),
    ("Summer", "Winter"),
    ("Day", "Night"),
    ("Sun", "Moon"),
    ("Ocean", "Desert"),
    ("Mountain", "Valley"),
    ("City", "Countryside"),
    ("Science", "Art"),
    ("Mind", "Body"),
]


class GameCondition(Enum):
    PLAYING = 0
    RED_WIN = 1
    BLUE_WIN = 2
    TIE = 3


class WavelengthGame:
    """Class that sets up game details and calls ClueGiver/Guesser pairs to play Wavelength"""

    def __init__(self, clue_giver_red, guesser_red, clue_giver_blue, guesser_blue,
                 seed="time", do_print=True, do_log=True, game_name="default",
                 cgr_kwargs={}, gsr_kwargs={}, cgb_kwargs={}, gsb_kwargs={},
                 single_team=False, max_rounds=5,
                 results_file="results/wavelength_results.txt"):
        """Setup Wavelength Game details

        Args:
            clue_giver_red (:class:`WavelengthClueGiver`):
                Clue giver for red team (Psychic) class that provides a clue.
            guesser_red (:class:`WavelengthGuesser`):
                Guesser for red team class that guesses based on clue.
            clue_giver_blue (:class:`WavelengthClueGiver`):
                Clue giver for blue team (Psychic) class that provides a clue.
            guesser_blue (:class:`WavelengthGuesser`):
                Guesser for blue team class that guesses based on clue.
            seed (int or str, optional):
                Value used to init random, "time" for time.time().
                Defaults to "time".
            do_print (bool, optional):
                Whether to keep on sys.stdout or turn off.
                Defaults to True.
            do_log (bool, optional):
                Whether to append to log file or not.
                Defaults to True.
            game_name (str, optional):
                game name used in log file. Defaults to "default".
            cgr_kwargs (dict, optional):
                kwargs passed to red ClueGiver.
            gsr_kwargs (dict, optional):
                kwargs passed to red Guesser.
            cgb_kwargs (dict, optional):
                kwargs passed to blue ClueGiver.
            gsb_kwargs (dict, optional):
                kwargs passed to blue Guesser.
            single_team (bool, optional):
                Whether to play the single team track version.
                Defaults to False.
            max_rounds (int, optional):
                Number of rounds to play. Defaults to 5.
        """

        self.game_winner = None
        self.game_start_time = time.time()
        self.game_end_time = None

        self.results_file = results_file
        self.do_print = do_print
        if not self.do_print:
            self._save_stdout = sys.stdout
            sys.stdout = open(os.devnull, 'w')

        self.clue_giver_red = clue_giver_red("Red", **cgr_kwargs)
        self.guesser_red = guesser_red("Red", **gsr_kwargs)
        self.clue_giver_blue = clue_giver_blue("Blue", **cgb_kwargs)
        self.guesser_blue = guesser_blue("Blue", **gsb_kwargs)

        self.cgr_kwargs = cgr_kwargs
        self.gsr_kwargs = gsr_kwargs
        self.cgb_kwargs = cgb_kwargs
        self.gsb_kwargs = gsb_kwargs
        self.do_log = do_log
        self.game_name = game_name
        self.single_team = single_team
        self.max_rounds = max_rounds

        self.move_history = []
        self.red_score = 0
        self.blue_score = 0

        if seed == 'time':
            self.seed = time.time()
            random.seed(self.seed)
        else:
            self.seed = seed
            random.seed(int(seed))

        print("seed:", self.seed)

    def __del__(self):
        if not self.do_print:
            sys.stdout.close()
            sys.stdout = self._save_stdout

    def _pick_spectrum(self):
        return random.choice(SPECTRUMS)

    def _pick_target(self):
        return random.randint(1, 100)

    def _calculate_score(self, target, guess):
        diff = abs(target - guess)
        if diff <= 5:
            return 4
        elif diff <= 15:
            return 3
        elif diff <= 30:
            return 2
        elif diff <= 50:
            return 1
        else:
            return 0

    def _display_spectrum(self, scale, target=None):
        bar_len = 40
        left, right = scale
        print(f"  {left:<20} {'─' * bar_len} {right:>20}")
        if target is not None:
            pos = int(target / 100 * bar_len)
            print(f"  {' ' * pos} ^ TARGET ({target})")

    def _play_turn(self, round_num, scale, target, team, clue_giver, guesser):
        print(f"\n{'=' * 60}")
        print(f"  ROUND {round_num} — {team} TEAM")
        print(f"{'=' * 60}\n")

        print(f"Spectrum:")
        self._display_spectrum(scale, target)
        print()

        clue_giver.set_game_state(scale, target)
        clue = clue_giver.get_clue()
        print(f"\n  {team} Psychic's clue: \"{clue}\"\n")

        print(f"{team} Guesser's turn:")
        self._display_spectrum(scale)
        print(f"  Clue: \"{clue}\"\n")

        move_history = self.get_move_history()
        guesser.set_move_history(move_history)
        guesser.set_scale(scale)
        guesser.set_clue(clue)
        guess = guesser.get_guess()

        diff = abs(target - guess)  # Calculate absolute difference directly

        print(f"\n  {'─' * 40}")
        print(f"    TARGET: {target}")
        print(f"    {team} GUESS: {guess}")
        print(f"    {team} DIFF: {diff}")
        print(f"  {'─' * 40}\n")

        move_record = {
            "round": round_num,
            "team": team,
            "scale": list(scale),
            "target": target,
            "clue": clue if isinstance(clue, str) else str(clue),
            "guess": guess,
            "diff": diff,
        }
        self.move_history.append(move_record)

        return diff  # Return absolute difference instead of score

    def get_move_history(self):
        return self.move_history

    def get_words_on_board(self):
        return None

    def run(self):
        print("\n" + "=" * 60)
        print("  WAVELENGTH")
        print("=" * 60 + "\n")

        for round_num in range(1, self.max_rounds + 1):
            scale = self._pick_spectrum()
            target = self._pick_target()

            red_score = self._play_turn(round_num, scale, target, "Red",
                                        self.clue_giver_red, self.guesser_red)
            self.red_score += red_score

            if not self.single_team:
                blue_score = self._play_turn(round_num, scale, target, "Blue",
                                             self.clue_giver_blue, self.guesser_blue)
                self.blue_score += blue_score

            print(f"  SCORES AFTER ROUND {round_num}:")
            print(f"    Red:  {self.red_score}")
            if not self.single_team:
                print(f"    Blue: {self.blue_score}")
            print()

        self.game_end_time = time.time()

        print("=" * 60)
        print("  FINAL RESULTS")
        print("=" * 60)
        print(f"    Red:  {self.red_score}")
        if not self.single_team:
            print(f"    Blue: {self.blue_score}")

            if self.red_score > self.blue_score:
                self.game_winner = "R"
                print("\n  *** RED TEAM WINS! ***")
            elif self.blue_score > self.red_score:
                self.game_winner = "B"
                print("\n  *** BLUE TEAM WINS! ***")
            else:
                self.game_winner = "T"
                print("\n  *** TIE! ***")
        else:
            self.game_winner = "R"
            print(f"\n  Single team mode — Red scored {self.red_score}")

        print()
        if self.do_log:
            self.write_results()
        print("Game Over\n")

    def write_results(self):
        # Create directory if it doesn't exist
        results_dir = os.path.dirname(self.results_file)
        if results_dir and not os.path.exists(results_dir):
            os.makedirs(results_dir, exist_ok=True)

        with open(self.results_file, "a") as f:
            f.write(
                f'ROUNDS:{self.max_rounds} '
                f'R:{self.red_score} B:{self.blue_score} '
                f'CLUE_GIVER_R:{self.clue_giver_red.__class__.__name__} '
                f'GUESSER_R:{self.guesser_red.__class__.__name__} '
                f'CLUE_GIVER_B:{self.clue_giver_blue.__class__.__name__} '
                f'GUESSER_B:{self.guesser_blue.__class__.__name__} '
                f'SEED:{self.seed} WINNER:{self.game_winner}\n'
            )

    @staticmethod
    def clear_results():
        if os.path.exists("results") and os.path.isdir("results"):
            import shutil
            shutil.rmtree("results")
