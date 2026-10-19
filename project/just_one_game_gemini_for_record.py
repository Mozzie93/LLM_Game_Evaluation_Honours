import argparse
import os
from just_one_game import JustOneGame
from players.just_one_clue_giver_GEMINI import AIJustOneClueGiver
from players.just_one_guesser_GEMINI import AIJustOneGuesser


def justOneExample(version="gemini-3.1-pro-preview"):
    # Sanitize version string (e.g., "gemini-3.1-pro-preview" -> "just_one_results_gemini-3_1-pro-preview.txt")
    safe_version = version.replace(".", "_").replace("/", "_")
    results_file = f"results/just_one_results_{safe_version}.txt"

    for i in range(30):
        seed = i

        print(f"starting Just One Gemini game with version: {version}")

        JustOneGame(AIJustOneClueGiver, AIJustOneGuesser,
                    seed=seed, do_print=True, game_name="Gemini-Gemini",
                    num_clue_givers=3, max_rounds=5,
                    cg_kwargs={"version": version}, g_kwargs={"version": version},
                    results_file=results_file).run()

        print(f"\nfor seed {seed} ~")
        if os.path.exists(results_file):
            with open(results_file) as f:
                for line in f.readlines():
                    print(line.strip())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Just One game with a specified Gemini model version.")
    parser.add_argument(
        "-v",
        "--version",
        type=str,
        default="gemini-3.1-pro-preview",
        help="Gemini model version to use (default: gemini-3.1-pro-preview)",
    )
    args = parser.parse_args()

    justOneExample(version=args.version)