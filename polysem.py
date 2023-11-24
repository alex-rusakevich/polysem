#!/usr/bin/env python3
import sys
from typing import Optional

from polysem.logics import sentence_to_best_meaning
from polysem.meanings import Meaning

MIN_PYTHON = (3, 8)

if sys.version_info < MIN_PYTHON:
    sys.exit("Python %s.%s or later is required.\n" % MIN_PYTHON)


def main():
    if len(sys.argv) == 1:  # REPL
        print("Press Ctrl-Z or Ctrl-C to stop")

        while True:
            sentence = input("Sentence: ")
            meaning: Optional[Meaning] = sentence_to_best_meaning(sentence)

            if meaning == None:
                print("Couldn't estimate the meaning, please, try another sentence")
            else:
                print("Meaning:", meaning.text)
                print("Example:", meaning.example)

            print()

    else:
        raise NotImplementedError("Command-line args are not supported yet")


if __name__ == "__main__":
    main()
