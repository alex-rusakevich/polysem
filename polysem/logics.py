import enum
import pathlib
import subprocess
from typing import List, Optional, Sequence, Union

from polysem import THE_WORD

from .meanings import *
from .meaningsign import MEANING_SEQ_MAX_SIZE, MEANING_SINGS, MeaningSeq, MeaningSign


def sentence_to_lemmas(sentence: str) -> Sequence[str]:
    mystem_path = pathlib.Path(__file__).parent.parent.resolve() / "mystem.exe"

    proc = subprocess.run(
        [mystem_path, "-ldn"], input=sentence.encode(), stdout=subprocess.PIPE
    )

    return proc.stdout.decode().replace("ё", "е").split()


def lemmas_to_meaning_seq(lemmas: Sequence[str]) -> MeaningSeq:
    def get_meaning_sign_by_lemma(lemma: str) -> Optional[MeaningSign]:
        if type(lemma) != str or lemma.strip() == "":
            return None

        for meaning_sign in MEANING_SINGS:
            if lemma == meaning_sign:
                return meaning_sign

        return None

    meaning_seq: Sequence[Any] = [None for _ in range(MEANING_SEQ_MAX_SIZE)]

    word_place = lemmas.index(THE_WORD)

    if word_place == -1:
        raise Exception(f"Core word has not been found: '{THE_WORD}'")

    meaning_seq[5] = THE_WORD

    # region Populate to left
    real_place = word_place - 1
    seq_place = 4

    while real_place >= 0 and seq_place >= 0:
        meaning_seq[seq_place] = get_meaning_sign_by_lemma(lemmas[real_place])

        real_place -= 1
        seq_place -= 1
    # endregion

    # region Populate to right
    real_place = word_place + 1
    seq_place = 6

    while real_place < len(lemmas) and seq_place < MEANING_SEQ_MAX_SIZE:
        meaning_seq[seq_place] = get_meaning_sign_by_lemma(lemmas[real_place])

        real_place += 1
        seq_place += 1
    # endregion

    return meaning_seq


def get_seq_meanings(sequence: MeaningSeq) -> List:
    found = {i: 0 for i, _ in enumerate(Meaning.instances)}
    found_smth = False

    for seq_elem in sequence:
        if isinstance(seq_elem, MeaningSign):
            found_index = -1

            for i, meaning_obj in enumerate(Meaning.instances):
                if meaning_obj == seq_elem.meaning:
                    found_index = i
                    found_smth = True
                    found[found_index] += 1

    if not found_smth:
        return []

    meaning_scores = sorted(found.items(), key=lambda x: x[1], reverse=True)

    result = []

    for i, (meaning_index, meaning_score) in enumerate(meaning_scores):
        if meaning_score != 0:
            meaning = None

            for i, meaning_obj in enumerate(Meaning.instances):
                if i == meaning_index:
                    meaning = meaning_obj

            result.append((meaning, meaning_score))

    return result


def sentence_to_best_meaning(sentence: str) -> Optional[Meaning]:
    meanings = get_seq_meanings(lemmas_to_meaning_seq(sentence_to_lemmas(sentence)))

    if len(meanings) == 0:
        return None
    else:
        return meanings[0][0]
