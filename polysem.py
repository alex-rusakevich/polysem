#!/usr/bin/env python3
import sys

import colorama
from colorama import Back, Fore, Style

from polysem.logics import *
from polysem.settings import *

MIN_PYTHON = (3, 8)

if sys.version_info < MIN_PYTHON:
    sys.exit("Python %s.%s or later is required.\n" % MIN_PYTHON)


colorama.init(autoreset=True)


def main():
    print(
        "The program was created by Alexander Rusakevich, 402/1, Chinese faculty (https://github.com/alex-rusakevich/polysem)"
    )
    the_yellow_word = Fore.YELLOW + "'" + THE_WORD + "'" + Style.RESET_ALL
    print(f"The core word is {the_yellow_word}")

    if len(sys.argv) == 1:  # REPL
        print("Press Ctrl-Z or Ctrl-C to stop")

        while True:
            stem_seqs = text_to_stem_seqs(
                input(Fore.YELLOW + "\nText: " + Style.RESET_ALL)
            )

            if stem_seqs == []:
                print(Fore.RED + f"No sentence with word '{THE_WORD}', skipping...")
                continue

            for orig_sent, sent_stems in stem_seqs:
                print(Fore.YELLOW + f"\nProcessing sentence '{orig_sent}'...")

                meanings = get_seq_meanings(stems_to_meaning_seq(sent_stems))

                if not meanings:
                    print(
                        Fore.RED
                        + "Couldn't estimate the meaning, please, try another sentence"
                    )
                    continue
                else:
                    for meaning, score in meanings:
                        print(
                            Fore.GREEN
                            + "\n-> "
                            + Style.RESET_ALL
                            + "Meaning with score "
                            + Fore.GREEN
                            + str(score)
                            + Style.RESET_ALL
                            + ":",
                            meaning.text,
                        )
                        print("Example:", meaning.example)

            print(Fore.GREEN + "\nDone.")

    else:
        raise NotImplementedError("Command-line args are not supported yet")


if __name__ == "__main__":
    main()
