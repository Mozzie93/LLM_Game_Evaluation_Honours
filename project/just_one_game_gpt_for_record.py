import argparse
import os
from just_one_game import JustOneGame
from players.just_one_clue_giver_GPT import AIJustOneClueGiver
from players.just_one_guesser_GPT import AIJustOneGuesser


def justOneExample(version="gpt-5.6-terra"):
    # Sanitize version string (e.g., "gpt-5.6-terra" -> "just_one_results_gpt-5_6-terra.txt")
    safe_version = version.replace(".", "_").replace("/", "_")
    results_file = f"results/just_one_results_{safe_version}.txt"

    for i in range(30):
        seed = i

        print(f"starting Just One GPT game with version: {version}")

        JustOneGame(AIJustOneClueGiver, AIJustOneGuesser,
                    seed=seed, do_print=True, game_name="GPT-GPT",
                    num_clue_givers=3, max_rounds=5,
                    cg_kwargs={"version": version}, g_kwargs={"version": version},
                    results_file=results_file).run()

        print(f"\nfor seed {seed} ~")
        if os.path.exists(results_file):
            with open(results_file) as f:
                for line in f.readlines():
                    print(line.strip())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Just One game with a specified GPT model version.")
    parser.add_argument(
        "-v",
        "--version",
        type=str,
        default="gpt-5.6-terra",
        help="GPT model version to use (default: gpt-5.6-terra)",
    )
    args = parser.parse_args()

    justOneExample(version=args.version)