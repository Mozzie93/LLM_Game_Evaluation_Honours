from just_one_game import JustOneGame
from players.just_one_clue_giver_CLAUDE import AIJustOneClueGiver
from players.just_one_guesser_CLAUDE import AIJustOneGuesser


def justOneExample():

    print("\nclearing results folder...\n")
    JustOneGame.clear_results()

    seed = 0

    print("starting Just One Claude game")
    JustOneGame(AIJustOneClueGiver, AIJustOneGuesser,
                seed=seed, do_print=True, game_name="Claude-Claude",
                num_clue_givers=3, max_rounds=5).run()

    print(f"\nfor seed {seed} ~")
    with open("results/just_one_results.txt") as f:
        for line in f.readlines():
            print(line.strip())


if __name__ == "__main__":
    justOneExample()
