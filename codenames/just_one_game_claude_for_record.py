import argparse
import os
from just_one_game import JustOneGame
from players.just_one_clue_giver_CLAUDE import AIJustOneClueGiver
from players.just_one_guesser_CLAUDE import AIJustOneGuesser


def justOneExample(version="claude-opus-5"):
    # Sanitize version string (e.g., "claude-opus-5" -> "just_one_results_claude-opus-5.txt")
    safe_version = version.replace(".", "_").replace("/", "_")
    results_file = f"results/just_one_results_{safe_version}.txt"

    for i in range(30):
        seed = i

        print(f"starting Just One Claude game with version: {version}")

        JustOneGame(AIJustOneClueGiver, AIJustOneGuesser,
                    seed=seed, do_print=True, game_name="Claude-Claude",
                    num_clue_givers=3, max_rounds=5,
                    cg_kwargs={"version": version}, g_kwargs={"version": version},
                    results_file=results_file).run()

        print(f"\nfor seed {seed} ~")
        if os.path.exists(results_file):
            with open(results_file) as f:
                for line in f.readlines():
                    print(line.strip())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Just One game with a specified Claude model version.")
    parser.add_argument(
        "-v",
        "--version",
        type=str,
        default="claude-opus-5",
        help="Claude model version to use (default: claude-opus-5)",
    )
    args = parser.parse_args()

    justOneExample(version=args.version)