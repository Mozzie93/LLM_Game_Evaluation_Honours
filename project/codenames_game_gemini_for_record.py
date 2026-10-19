import argparse
import os
import json
from game import Game
from players.codemaster_GEMINI import GeminiCodemaster
from players.guesser_GEMINI import GeminiGuesser


def simpleExample(single_team, version="gemini-3.1-pro-preview"):
    # Sanitize version string (e.g., "gemini-3.1-pro-preview" -> "codenames_results_gemini-3_1-pro-preview.txt")
    safe_version = version.replace(".", "_").replace("/", "_")
    results_file = f"results/codenames_results_{safe_version}.txt"

    for i in range(30):
        seed = i

        print(f"starting Codenames Gemini game with version: {version}")

        Game(GeminiCodemaster, GeminiGuesser, GeminiCodemaster, GeminiGuesser,
             seed=seed, do_print=True, game_name="Gemini-Gemini",
             single_team=single_team,
             cmr_kwargs={"version": version}, gr_kwargs={"version": version},
             cmb_kwargs={"version": version}, gb_kwargs={"version": version},
             results_file=results_file).run()

        print(f"\nfor seed {seed} ~")
        if os.path.exists(results_file):
            with open(results_file) as f:
                for line in f.readlines():
                    game_json = json.loads(line.rstrip())
                    game_name = game_json["game_name"]
                    game_time = game_json["time_s"]
                    game_score = game_json["total_turns"]
                    game_winner = game_json["winner"]
                    print(f"time={game_time:.2f}, turns={game_score}, name={game_name}, winner={game_winner}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Codenames game with a specified Gemini model version.")
    parser.add_argument(
        "-v",
        "--version",
        type=str,
        default="gemini-3.1-pro-preview",
        help="Gemini model version to use (default: gemini-3.1-pro-preview)",
    )
    args = parser.parse_args()

    simpleExample(True, version=args.version)