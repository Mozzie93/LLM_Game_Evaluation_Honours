import argparse
import os
from wavelength_game import WavelengthGame
from players.wavelength_clue_giver_CLAUDE import AIWavelengthClueGiver
from players.wavelength_guesser_CLAUDE import AIWavelengthGuesser


def wavelengthExample(single_team, version="claude-haiku-4-5"):
    # Sanitize version string (e.g., "claude-haiku-4.5" -> "wavelength_results_claude-haiku-4_5.txt")
    safe_version = version.replace(".", "_").replace("/", "_")
    results_file = f"results/wavelength_results_{safe_version}.txt"

    for i in range(30):
        seed = i

        print(f"starting Wavelength Claude game with version: {version}")

        clue_giver = lambda team="Red": AIWavelengthClueGiver(team=team, version=version)
        guesser = lambda team="Red": AIWavelengthGuesser(team=team, version=version)

        WavelengthGame(
            clue_giver,
            guesser,
            clue_giver,
            guesser,
            seed=seed,
            do_print=True,
            game_name="Claude-Claude",
            single_team=single_team,
            max_rounds=3,
            results_file=results_file,  # Pass dynamic filename
        ).run()

        print(f"\nfor seed {seed} ~")
        if os.path.exists(results_file):
            with open(results_file) as f:
                for line in f.readlines():
                    print(line.strip())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Wavelength game with a specified Claude model version.")
    parser.add_argument(
        "-v",
        "--version",
        type=str,
        default="claude-haiku-4-5",
        help="Claude model version to use (default: claude-haiku-4-5)",
    )
    args = parser.parse_args()

    wavelengthExample(True, version=args.version)