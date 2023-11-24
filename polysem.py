#!/usr/bin/env python3
import sys

from polysem.logics import *

MIN_PYTHON = (3, 8)

if sys.version_info < MIN_PYTHON:
    sys.exit("Python %s.%s or later is required.\n" % MIN_PYTHON)


def main():
    if len(sys.argv) == 1:  # REPL
        print("Press Ctrl-Z or Ctrl-C to stop")

        while True:
            sentence = input("Sentence: ")
            meanings = get_seq_meanings(
                lemmas_to_meaning_seq(sentence_to_lemmas(sentence))
            )

            if not meanings:
                print("Couldn't estimate the meaning, please, try another sentence")
            else:
                for meaning, score in meanings:
                    print(f"\nMeaning with score {score}:", meaning.text)
                    print("Example:", meaning.example)
                    print()

    else:
        raise NotImplementedError("Command-line args are not supported yet")


if __name__ == "__main__":
    main()
