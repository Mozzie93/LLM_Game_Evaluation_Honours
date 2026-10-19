import argparse
import os
from wavelength_game import WavelengthGame
from players.wavelength_clue_giver_GPT import AIWavelengthClueGiver
from players.wavelength_guesser_GPT import AIWavelengthGuesser


def wavelengthExample(single_team, version="gpt-5.6-terra"):
    # Sanitize version string (e.g., "gpt-5.6-terra" -> "wavelength_results_gpt-5.6-terra.txt")
    safe_version = version.replace(".", "_").replace("/", "_")
    results_file = f"results/wavelength_results_{safe_version}.txt"

    for i in range(30):
        seed = i

        print(f"starting Wavelength GPT game with version: {version}")

        clue_giver = lambda team="Red": AIWavelengthClueGiver(team=team, version=version)
        guesser = lambda team="Red": AIWavelengthGuesser(team=team, version=version)

        WavelengthGame(
            clue_giver,
            guesser,
            clue_giver,
            guesser,
            seed=seed,
            do_print=True,
            game_name="GPT-GPT",
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
    parser = argparse.ArgumentParser(description="Run Wavelength game with a specified GPT model version.")
    parser.add_argument(
        "-v",
        "--version",
        type=str,
        default="gpt-5.6-terra",
        help="GPT model version to use (default: gpt-5.6-terra)",
    )
    args = parser.parse_args()

    wavelengthExample(True, version=args.version)