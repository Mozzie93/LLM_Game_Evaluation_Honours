import random
import time
import json
import os
import sys
from enum import Enum


class GameCondition(Enum):
    PLAYING = 0
    RED_WIN = 1
    BLUE_WIN = 2
    TIE = 3


class DecryptoGame:
    """Class that sets up game details and calls Encryptor/Decryptor pairs to play Decrypto"""

    def __init__(self, encryptor_red, decryptor_red, encryptor_blue, decryptor_blue,
                 seed="time", do_print=True, do_log=True, game_name="default",
                 er_kwargs={}, dr_kwargs={}, eb_kwargs={}, db_kwargs={},
                 single_team=False, max_rounds=8,
                 interception_win=2, miscomm_loss=3,
                 results_file="results/decrypto_results.txt"):
        """
        Args:
            encryptor_red (:class:`DecryptoEncryptor`):
                Encryptor for red team class that provides clues.
            decryptor_red (:class:`DecryptoDecryptor`):
                Decryptor/Interceptor for red team.
            encryptor_blue (:class:`DecryptoEncryptor`):
                Encryptor for blue team class that provides clues.
            decryptor_blue (:class:`DecryptoDecryptor`):
                Decryptor/Interceptor for blue team.
            seed (int or str, optional):
                Value used to init random, "time" for time.time(). Defaults to "time".
            do_print (bool, optional):
                Whether to keep on sys.stdout or turn off. Defaults to True.
            do_log (bool, optional):
                Whether to append to log file or not. Defaults to True.
            game_name (str, optional):
                game name used in log file. Defaults to "default".
            er_kwargs (dict, optional):
                kwargs passed to red Encryptor.
            dr_kwargs (dict, optional):
                kwargs passed to red Decryptor.
            eb_kwargs (dict, optional):
                kwargs passed to blue Encryptor.
            db_kwargs (dict, optional):
                kwargs passed to blue Decryptor.
            single_team (bool, optional):
                Whether to play the single team track version. Defaults to False.
            max_rounds (int, optional):
                Number of rounds to play. Defaults to 8.
            interception_win (int, optional):
                Number of successful interceptions to win. Defaults to 2.
            miscomm_loss (int, optional):
                Number of miscommunications to lose. Defaults to 3.
        """

        self.game_winner = None
        self.game_start_time = time.time()
        self.game_end_time = None

        self.do_print = do_print
        if not self.do_print:
            self._save_stdout = sys.stdout
            sys.stdout = open(os.devnull, 'w')

        self.encryptor_red = encryptor_red("Red", **er_kwargs)
        self.decryptor_red = decryptor_red("Red", **dr_kwargs)
        self.encryptor_blue = encryptor_blue("Blue", **eb_kwargs)
        self.decryptor_blue = decryptor_blue("Blue", **db_kwargs)

        self.er_kwargs = er_kwargs
        self.dr_kwargs = dr_kwargs
        self.eb_kwargs = eb_kwargs
        self.db_kwargs = db_kwargs
        self.do_log = do_log
        self.game_name = game_name
        self.single_team = single_team
        self.max_rounds = max_rounds
        self.interception_win = interception_win
        self.miscomm_loss = miscomm_loss
        self.results_file = results_file

        self.red_code_words = []
        self.blue_code_words = []

        self.red_clue_history = []
        self.blue_clue_history = []

        self.red_miscommunications = 0
        self.blue_miscommunications = 0
        self.red_interceptions = 0
        self.blue_interceptions = 0

        self.move_history = []

        if seed == 'time':
            self.seed = time.time()
            random.seed(self.seed)
        else:
            self.seed = seed
            random.seed(int(seed))

        print("seed:", self.seed)

        self._pick_code_words()

    def __del__(self):
        if not self.do_print:
            sys.stdout.close()
            sys.stdout = self._save_stdout

    def _pick_code_words(self):
        list_path = os.path.join(os.path.dirname(__file__), "players", "cm_wordlist.txt")
        with open(list_path, "r") as f:
            all_words = [w.strip() for w in f.read().splitlines() if w.strip()]
        random.shuffle(all_words)
        needed = 8 if not self.single_team else 4
        if len(all_words) < needed:
            raise ValueError(f"Not enough words in word list (need {needed}, have {len(all_words)})")
        self.red_code_words = all_words[:4]
        if not self.single_team:
            self.blue_code_words = all_words[4:8]
        else:
            self.blue_code_words = []

    def _generate_sequence(self):
        return random.sample(range(1, 5), 3)

    def _format_clue_history(self, history):
        lines = []
        for i, entry in enumerate(history, 1):
            lines.append(f"  Round {i}: clues = {entry['clues']}, sequence = {entry['sequence']}")
        return "\n".join(lines)

    def _request_clues(self, encryptor, clue_history):
        """Get clues from the encryptor, enforcing that no clue is ever repeated.

        Any clue that was already used in a previous round is rejected and the
        encryptor is asked to provide fresh clues instead.
        """
        used_clues = set()
        for entry in clue_history:
            for clue in entry.get("clues", []):
                used_clues.add(str(clue).strip().lower())

        def is_fresh(cands):
            normalized = [c.strip().lower() for c in cands]
            return (all(c not in used_clues for c in normalized)
                    and len(set(normalized)) == len(normalized))

        clues = encryptor.get_clue()
        attempts = 0
        while not is_fresh(clues) and attempts < 5:
            attempts += 1
            normalized = [c.strip().lower() for c in clues]
            repeated = [c for i, c in enumerate(normalized)
                        if c in used_clues or c in normalized[:i]]
            print(f"  *** RULE VIOLATION: clue(s) {repeated} repeat a previously used/current clue. "
                  "Requesting fresh clues. ***")
            if hasattr(encryptor, "block_clues"):
                encryptor.block_clues(repeated)
            clues = encryptor.get_clue()
        if attempts > 0:
            print("  *** Fresh clues obtained after enforcing the no-repeat rule. ***")
        return clues

    def _play_team_turn(self, round_num, team_name, encryptor, decryptor,
                        interceptor, code_words, opp_code_words,
                        clue_history, opp_clue_history):
        sequence = self._generate_sequence()
        seq_str = f"{sequence[0]}-{sequence[1]}-{sequence[2]}"

        print(f"\n{'=' * 60}")
        print(f"  ROUND {round_num} — {team_name} TEAM TRANSMITS")
        print(f"{'=' * 60}\n")

        print(f"{team_name} code words:")
        for i, w in enumerate(code_words, 1):
            print(f"  {i}: {w}")

        encryptor.set_game_state(code_words, sequence)
        encryptor.set_move_history(clue_history)
        clues = self._request_clues(encryptor, clue_history)
        print(f"\n  {team_name} Encryptor's clues: {clues[0]} / {clues[1]} / {clues[2]}\n")

        decryptor.set_code_words(code_words)
        decryptor.set_clues(clues)
        decryptor.set_move_history(clue_history)
        team_guess = decryptor.get_guess()
        team_guess_str = f"{team_guess[0]}-{team_guess[1]}-{team_guess[2]}"
        print(f"\n  {team_name} Decryptor guessed: {team_guess_str}")

        decryptor_correct = (team_guess == sequence)
        if decryptor_correct:
            print(f"  ✓ {team_name} Decryptor CORRECT!")
        else:
            print(f"  ✗ {team_name} Decryptor INCORRECT (was {seq_str})")

        interceptor.set_code_words(None)
        interceptor.set_clues(clues)
        interceptor.set_move_history(opp_clue_history)
        intercept_guess = interceptor.get_interception_guess()
        intercept_str = f"{intercept_guess[0]}-{intercept_guess[1]}-{intercept_guess[2]}"
        print(f"\n  Opponent Interceptor guessed: {intercept_str}")

        interceptor_correct = (intercept_guess == sequence)
        if interceptor_correct:
            print(f"  ✓ Opponent Interceptor CORRECT!")
        else:
            print(f"  ✗ Opponent Interceptor INCORRECT")

        miscommunication = not decryptor_correct
        interception = interceptor_correct

        if miscommunication:
            if team_name == "Red":
                self.red_miscommunications += 1
            else:
                self.blue_miscommunications += 1
            print(f"  *** MISCOMMUNICATION for {team_name} ***")

        if interception:
            if team_name == "Red":
                self.blue_interceptions += 1
                interceptor_team = "Blue"
            else:
                self.red_interceptions += 1
                interceptor_team = "Red"
            print(f"  *** INTERCEPTION by {interceptor_team} ***")

        move_record = {
            "round": round_num,
            "team": team_name,
            "code_words": list(code_words),
            "sequence": list(sequence),
            "clues": list(clues),
            "team_guess": team_guess,
            "team_correct": decryptor_correct,
            "intercept_guess": intercept_guess,
            "intercept_correct": interceptor_correct,
        }
        self.move_history.append(move_record)
        clue_history.append({"round": round_num, "clues": list(clues), "sequence": list(sequence)})
        opp_clue_history.append({"round": round_num, "clues": list(clues), "sequence": list(sequence)})

        self._display_scores()

        return miscommunication, interception

    def _display_scores(self):
        print(f"\n  {'─' * 40}")
        print(f"  SCORES:")
        print(f"    Red:  {self.red_miscommunications} miscommunications, "
              f"{self.red_interceptions} interceptions")
        if not self.single_team:
            print(f"    Blue: {self.blue_miscommunications} miscommunications, "
                  f"{self.blue_interceptions} interceptions")
        print(f"  {'─' * 40}")

    def _check_win_condition(self):
        if not self.single_team:
            if self.blue_interceptions >= self.interception_win:
                return GameCondition.BLUE_WIN
            if self.red_interceptions >= self.interception_win:
                return GameCondition.RED_WIN
            if self.red_miscommunications >= self.miscomm_loss:
                return GameCondition.BLUE_WIN
            if self.blue_miscommunications >= self.miscomm_loss:
                return GameCondition.RED_WIN
        return GameCondition.PLAYING

    def run(self):
        print("\n" + "=" * 60)
        print("  DECRYPTO")
        print("=" * 60 + "\n")

        print("Red team code words:")
        for i, w in enumerate(self.red_code_words, 1):
            print(f"  {i}: {w}")
        if not self.single_team:
            print("\nBlue team code words:")
            for i, w in enumerate(self.blue_code_words, 1):
                print(f"  {i}: {w}")
        print()

        game_condition = GameCondition.PLAYING

        for round_num in range(1, self.max_rounds + 1):
            miscomm_red, inter_red = self._play_team_turn(
                round_num, "Red",
                self.encryptor_red, self.decryptor_red, self.decryptor_blue,
                self.red_code_words, self.blue_code_words,
                self.red_clue_history, self.blue_clue_history
            )

            game_condition = self._check_win_condition()
            if game_condition != GameCondition.PLAYING:
                break

            if not self.single_team:
                miscomm_blue, inter_blue = self._play_team_turn(
                    round_num, "Blue",
                    self.encryptor_blue, self.decryptor_blue, self.decryptor_red,
                    self.blue_code_words, self.red_code_words,
                    self.blue_clue_history, self.red_clue_history
                )

                game_condition = self._check_win_condition()
                if game_condition != GameCondition.PLAYING:
                    break

        self.game_end_time = time.time()

        print("\n" + "=" * 60)
        print("  FINAL RESULTS")
        print("=" * 60)
        print(f"    Red:  {self.red_miscommunications} miscommunications, "
              f"{self.red_interceptions} interceptions")
        if not self.single_team:
            print(f"    Blue: {self.blue_miscommunications} miscommunications, "
                  f"{self.blue_interceptions} interceptions")

            if game_condition == GameCondition.RED_WIN:
                self.game_winner = "R"
                print("\n  *** RED TEAM WINS! ***")
            elif game_condition == GameCondition.BLUE_WIN:
                self.game_winner = "B"
                print("\n  *** BLUE TEAM WINS! ***")
            else:
                self.game_winner = "T"
                print("\n  *** TIE — Max rounds reached ***")
        else:
            self.game_winner = "R"
            print(f"\n  Single team mode — Red completed {len(self.red_clue_history)} rounds")

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
                f'ROUNDS:{len(self.red_clue_history)} '
                f'R_MISC:{self.red_miscommunications} R_INT:{self.red_interceptions} '
                f'B_MISC:{self.blue_miscommunications} B_INT:{self.blue_interceptions} '
                f'ENCRYPTOR_R:{self.encryptor_red.__class__.__name__} '
                f'DECRYPTOR_R:{self.decryptor_red.__class__.__name__} '
                f'ENCRYPTOR_B:{self.encryptor_blue.__class__.__name__} '
                f'DECRYPTOR_B:{self.decryptor_blue.__class__.__name__} '
                f'SEED:{self.seed} WINNER:{self.game_winner}\n'
            )

    @staticmethod
    def clear_results():
        if os.path.exists("results") and os.path.isdir("results"):
            import shutil
            shutil.rmtree("results")
