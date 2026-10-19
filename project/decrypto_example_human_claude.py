from decrypto_game import DecryptoGame
from players.decrypto_encryptor_CLAUDE import AIDecryptoEncryptor
from players.decrypto_decryptor import HumanDecryptoDecryptor


def decryptoExample(single_team):

    print("\nclearing results folder...\n")
    DecryptoGame.clear_results()

    seed = 0

    print("starting Decrypto Claude vs Human game")
    DecryptoGame(AIDecryptoEncryptor, HumanDecryptoDecryptor,
                 AIDecryptoEncryptor, HumanDecryptoDecryptor,
                 seed=seed, do_print=True, game_name="Claude-Human",
                 single_team=single_team, max_rounds=8).run()

    print(f"\nfor seed {seed} ~")
    with open("results/decrypto_results.txt") as f:
        for line in f.readlines():
            print(line.strip())


if __name__ == "__main__":
    decryptoExample(True)     # Single Team Track
