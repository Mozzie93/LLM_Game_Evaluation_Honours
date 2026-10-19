import random
import time
import json
import os
import sys
from enum import Enum


class JustOneGame:
    """Cooperative word-association game where clue-givers help a guesser identify mystery words."""

    def __init__(self, clue_giver_class, guesser_class,
                 seed="time", do_print=True, do_log=True, game_name="default",
                 cg_kwargs={}, g_kwargs={},
                 num_clue_givers=3, max_rounds=13,
                 results_file="results/just_one_results.txt"):
        """
        Args:
            clue_giver_class (:class:`JustOneClueGiver`):
                Class for clue-giver AI instances.
            guesser_class (:class:`JustOneGuesser`):
                Class for the guesser AI instance.
            seed (int or str, optional):
                Value used to init random, "time" for time.time(). Defaults to "time".
            do_print (bool, optional):
                Whether to keep on sys.stdout or turn off. Defaults to True.
            do_log (bool, optional):
                Whether to append to log file or not. Defaults to True.
            game_name (str, optional):
                game name used in log file. Defaults to "default".
            cg_kwargs (dict, optional):
                kwargs passed to clue-giver instances.
            g_kwargs (dict, optional):
                kwargs passed to guesser instance.
            num_clue_givers (int, optional):
                Number of clue-giver AI instances per round. Defaults to 3.
            max_rounds (int, optional):
                Number of rounds to play. Defaults to 13.
            results_file (str, optional):
                Path to the results log file. Defaults to "results/just_one_results.txt".
        """

        self.game_score = 0
        self.game_total = 0
        self.game_start_time = time.time()
        self.game_end_time = None

        self.do_print = do_print
        if not self.do_print:
            self._save_stdout = sys.stdout
            sys.stdout = open(os.devnull, 'w')

        self.num_clue_givers = num_clue_givers
        self.clue_givers = [clue_giver_class(f"ClueGiver_{i+1}", **cg_kwargs)
                            for i in range(num_clue_givers)]
        self.guesser = guesser_class("Guesser", **g_kwargs)

        self.cg_kwargs = cg_kwargs
        self.g_kwargs = g_kwargs
        self.do_log = do_log
        self.game_name = game_name
        self.max_rounds = max_rounds
        self.results_file = results_file

        self.move_history = []

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

    def _pick_target_word(self, used_words):
        list_path = os.path.join(os.path.dirname(__file__), "players", "cm_wordlist.txt")
        with open(list_path, "r") as f:
            all_words = [w.strip() for w in f.read().splitlines() if w.strip()]
        available = [w for w in all_words if w not in used_words]
        if not available:
            available = all_words
        return random.choice(available)

    def _normalize_clue(self, clue):
        return clue.strip().lower().strip(".,!?\"';:")

    def _remove_duplicates(self, clues):
        counts = {}
        for clue in clues:
            normalized = self._normalize_clue(clue)
            counts[normalized] = counts.get(normalized, 0) + 1
        unique = []
        for clue in clues:
            normalized = self._normalize_clue(clue)
            if counts[normalized] == 1:
                unique.append(clue)
            else:
                print(f"  (removed duplicate: \"{clue}\")")
        return unique

    def _play_round(self, round_num, target_word):
        print(f"\n{'=' * 60}")
        print(f"  ROUND {round_num} — TARGET: ???")
        print(f"{'=' * 60}\n")

        for i, cg in enumerate(self.clue_givers):
            cg.set_target_word(target_word)

        raw_clues = []
        for i, cg in enumerate(self.clue_givers):
            clue = cg.get_clue()
            raw_clues.append(clue)

        print(f"\n  Raw clues: {raw_clues}")

        unique_clues = self._remove_duplicates(raw_clues)
        print(f"  Unique clues: {unique_clues}")

        if not unique_clues:
            print("  All clues were duplicates — no clues available!")
            self.guesser.set_clues([])
        else:
            self.guesser.set_clues(unique_clues)

        guess = self.guesser.get_guess()
        guess_lower = guess.lower().strip()

        correct = guess_lower == target_word.lower()
        if correct:
            print(f"\n  ✓ CORRECT! The word was: {target_word}")
            self.game_score += 1
        else:
            if guess_lower == "pass":
                print(f"\n  — PASSED. The word was: {target_word}")
            else:
                print(f"\n  ✗ INCORRECT. The word was: {target_word}")
        self.game_total += 1

        move_record = {
            "round": round_num,
            "target": target_word,
            "raw_clues": list(raw_clues),
            "unique_clues": unique_clues,
            "guess": guess,
            "correct": correct,
        }
        self.move_history.append(move_record)

        print(f"\n  Score: {self.game_score}/{self.game_total}")

    def run(self):
        print("\n" + "=" * 60)
        print("  JUST ONE")
        print("=" * 60 + "\n")

        used_words = set()

        for round_num in range(1, self.max_rounds + 1):
            target_word = self._pick_target_word(used_words)
            used_words.add(target_word)
            self._play_round(round_num, target_word)

        self.game_end_time = time.time()

        print("\n" + "=" * 60)
        print("  FINAL RESULTS")
        print("=" * 60)
        print(f"  Score: {self.game_score}/{self.game_total}")
        pct = (self.game_score / self.game_total * 100) if self.game_total > 0 else 0
        print(f"  Accuracy: {pct:.1f}%")
        print()
        if self.do_log:
            self.write_results()
        print("Game Over\n")

    def write_results(self):
        results_dir = os.path.dirname(self.results_file)
        if results_dir and not os.path.exists(results_dir):
            os.makedirs(results_dir, exist_ok=True)

        with open(self.results_file, "a") as f:
            f.write(
                f'ROUNDS:{self.max_rounds} '
                f'SCORE:{self.game_score}/{self.game_total} '
                f'ACCURACY:{(self.game_score / self.game_total * 100) if self.game_total > 0 else 0:.1f}% '
                f'CLUE_GIVERS:{self.num_clue_givers} '
                f'CG_CLASS:{self.clue_givers[0].__class__.__name__} '
                f'GUESSER_CLASS:{self.guesser.__class__.__name__} '
                f'SEED:{self.seed}\n'
            )

    @staticmethod
    def clear_results():
        if os.path.exists("results") and os.path.isdir("results"):
            import shutil
            shutil.rmtree("results")
