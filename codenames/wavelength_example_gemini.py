from wavelength_game import WavelengthGame
from players.wavelength_clue_giver_GEMINI import AIWavelengthClueGiver
from players.wavelength_guesser_GEMINI import AIWavelengthGuesser


def wavelengthExample(single_team):

    print("\nclearing results folder...\n")
    WavelengthGame.clear_results()

    seed = 0

    print("starting Wavelength Gemini game")
    WavelengthGame(AIWavelengthClueGiver, AIWavelengthGuesser,
                   AIWavelengthClueGiver, AIWavelengthGuesser,
                   seed=seed, do_print=True, game_name="Gemini-Gemini",
                   single_team=single_team, max_rounds=3).run()

    print(f"\nfor seed {seed} ~")
    with open("results/wavelength_results.txt") as f:
        for line in f.readlines():
            print(line.strip())


if __name__ == "__main__":
    wavelengthExample(False)    # Two Teams Track
    wavelengthExample(True)     # Single Team Track
