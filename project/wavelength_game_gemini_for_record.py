import argparse
import os
from wavelength_game import WavelengthGame
from players.wavelength_clue_giver_GEMINI import AIWavelengthClueGiver
from players.wavelength_guesser_GEMINI import AIWavelengthGuesser


def wavelengthExample(single_team, version="gemini-3.5-flash-lite"):
    # Sanitize version string (e.g., "gemini-3.5-flash-lite" -> "wavelength_results_gemini-3.5-flash-lite.txt")
    safe_version = version.replace(".", "_").replace("/", "_")
    results_file = f"results/wavelength_results_{safe_version}.txt"

    for i in range(30):
        seed = i

        print(f"starting Wavelength Gemini game with version: {version}")

        clue_giver = lambda team="Red": AIWavelengthClueGiver(team=team, version=version)
        guesser = lambda team="Red": AIWavelengthGuesser(team=team, version=version)

        WavelengthGame(
            clue_giver,
            guesser,
            clue_giver,
            guesser,
            seed=seed,
            do_print=True,
            game_name="Gemini-Gemini",
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
    parser = argparse.ArgumentParser(description="Run Wavelength game with a specified Gemini model version.")
    parser.add_argument(
        "-v",
        "--version",
        type=str,
        default="gemini-3.5-flash-lite",
        help="Gemini model version to use (default: gemini-3.5-flash-lite)",
    )
    args = parser.parse_args()

    wavelengthExample(True, version=args.version)