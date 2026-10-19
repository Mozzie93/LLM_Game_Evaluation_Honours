from decrypto_game import DecryptoGame
from players.decrypto_encryptor_GPT import AIDecryptoEncryptor
from players.decrypto_decryptor_GPT import AIDecryptoDecryptor


def decryptoExample(single_team):

    print("\nclearing results folder...\n")
    DecryptoGame.clear_results()

    seed = 0

    print("starting Decrypto GPT game")
    DecryptoGame(AIDecryptoEncryptor, AIDecryptoDecryptor,
                 AIDecryptoEncryptor, AIDecryptoDecryptor,
                 seed=seed, do_print=True, game_name="GPT-GPT",
                 single_team=single_team, max_rounds=8).run()

    print(f"\nfor seed {seed} ~")
    with open("results/decrypto_results.txt") as f:
        for line in f.readlines():
            print(line.strip())


if __name__ == "__main__":
    decryptoExample(False)    # Two Teams Track
    decryptoExample(True)     # Single Team Track
