import argparse
import os
from decrypto_game import DecryptoGame
from players.decrypto_encryptor_CLAUDE import AIDecryptoEncryptor
from players.decrypto_decryptor_CLAUDE import AIDecryptoDecryptor
from players.decrypto_decryptor_DEEPSEEK import AIDecryptoDecryptor as AIDecryptoInterceptor


def decryptoExample(single_team, version="claude-haiku-4-5", deepseek_version="deepseek-chat"):
    # Sanitize version string (e.g., "claude-haiku-4.5" -> "decrypto_results_claude-haiku-4_5.txt")
    safe_version = version.replace(".", "_").replace("/", "_")
    results_file = f"results/decrypto_results_{safe_version}.txt"

    for i in range(30):
        seed = i

        print(f"starting Decrypto Claude game with version: {version}")

        encryptor = lambda team="Red": AIDecryptoEncryptor(team=team, version=version)
        decryptor = lambda team="Red": AIDecryptoDecryptor(team=team, version=version)
        interceptor = lambda team="Blue": AIDecryptoInterceptor(team=team, version=deepseek_version)

        DecryptoGame(
            encryptor,
            decryptor,
            encryptor,
            interceptor,
            seed=seed,
            do_print=True,
            game_name="Claude-Claude",
            single_team=single_team,
            max_rounds=8,
            results_file=results_file,  # Pass dynamic filename
        ).run()

        print(f"\nfor seed {seed} ~")
        if os.path.exists(results_file):
            with open(results_file) as f:
                for line in f.readlines():
                    print(line.strip())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Decrypto game with a specified Claude model version.")
    parser.add_argument(
        "-v",
        "--version",
        type=str,
        default="claude-haiku-4-5",
        help="Claude model version to use (default: claude-haiku-4-5)",
    )
    parser.add_argument(
        "--deepseek-version",
        type=str,
        default="deepseek-chat",
        help="DeepSeek model version to use for the interceptor role (default: deepseek-chat)",
    )
    args = parser.parse_args()

    decryptoExample(True, version=args.version, deepseek_version=args.deepseek_version)