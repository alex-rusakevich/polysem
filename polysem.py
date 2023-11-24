#!/usr/bin/env python3
import sys

from polysem import THE_WORD
from polysem.logics import *

MIN_PYTHON = (3, 8)

if sys.version_info < MIN_PYTHON:
    sys.exit("Python %s.%s or later is required.\n" % MIN_PYTHON)


def main():
    print("The program was created by Alexander Rusakevich, 402/1, Chinese faculty")
    print(f"The core word is '{THE_WORD}'")

    if len(sys.argv) == 1:  # REPL
        print("Press Ctrl-Z or Ctrl-C to stop")

        while True:
            lemma_seqs = text_to_lemma_seqs(input("\nText: "))

            if lemma_seqs == []:
                print(f"No sentence with word '{THE_WORD}', skipping...")
                continue

            for orig_sent, sent_lemmas in lemma_seqs:
                print(f"\nProcessing sentence '{orig_sent}'...")

                meanings = get_seq_meanings(lemmas_to_meaning_seq(sent_lemmas))

                if not meanings:
                    print("Couldn't estimate the meaning, please, try another sentence")
                else:
                    for meaning, score in meanings:
                        print(f"\nMeaning with score {score}:", meaning.text)
                        print("Example:", meaning.example)

            print("\nDone.")

    else:
        raise NotImplementedError("Command-line args are not supported yet")


if __name__ == "__main__":
    main()
