import pathlib
import subprocess
from typing import List, Optional, Sequence, Tuple

import nltk

from polysem.settings import *

from .meanings import *


def sentence_to_stems(sentence: str) -> Sequence[str]:
    mystem_path = pathlib.Path(__file__).parent.parent.resolve() / "mystem.exe"

    proc = subprocess.run(
        [mystem_path, "-ldn"], input=sentence.encode(), stdout=subprocess.PIPE
    )

    return proc.stdout.decode().replace("ё", "е").split()


def split_text_into_sentences(text: str) -> Sequence[str]:
    return nltk.tokenize.sent_tokenize(text, language="russian")


def text_to_stem_seqs(text: str) -> Sequence[Tuple]:
    result = []

    for sent in split_text_into_sentences(text):
        sent_stems = sentence_to_stems(sent)
        if THE_WORD in sent_stems:
            result.append((sent, sent_stems))

    return result


def stems_to_meaning_seq(stems: Sequence[str]) -> MeaningSeq:
    def get_meaning_sign_by_stem(stem: str) -> Optional[MeaningSign]:
        if type(stem) != str or stem.strip() == "":
            return None

        for meaning_sign in MEANING_SINGS:
            if stem == meaning_sign:
                return meaning_sign

        return None

    meaning_seq: Sequence[Any] = [None for _ in range(MEANING_SEQ_MAX_SIZE)]

    word_place = stems.index(THE_WORD)

    if word_place == -1:
        raise Exception(f"Core word has not been found: '{THE_WORD}'")

    meaning_seq[5] = THE_WORD

    # region Populate to left
    real_place = word_place - 1
    seq_place = 4

    while real_place >= 0 and seq_place >= 0:
        potential_meaning = get_meaning_sign_by_stem(stems[real_place])

        if potential_meaning and potential_meaning.left_pos:
            distance_from_word = word_place - real_place

            if (
                type(potential_meaning.left_pos) == int
                and potential_meaning.left_pos == distance_from_word
            ):
                meaning_seq[seq_place] = potential_meaning
            elif type(potential_meaning.left_pos) in (
                list,
                tuple,
            ) and distance_from_word in range(
                potential_meaning.left_pos[0], potential_meaning.left_pos[1] + 1
            ):
                meaning_seq[seq_place] = potential_meaning

        real_place -= 1
        seq_place -= 1
    # endregion

    # region Populate to right
    real_place = word_place + 1
    seq_place = 6

    while real_place < len(stems) and seq_place < MEANING_SEQ_MAX_SIZE:
        potential_meaning = get_meaning_sign_by_stem(stems[real_place])

        if potential_meaning and potential_meaning.right_pos:
            distance_from_word = real_place - word_place

            if (
                type(potential_meaning.right_pos) == int
                and potential_meaning.right_pos == distance_from_word
            ):
                meaning_seq[seq_place] = potential_meaning
            elif type(potential_meaning.right_pos) in (
                list,
                tuple,
            ) and distance_from_word in range(
                potential_meaning.right_pos[0], potential_meaning.right_pos[1] + 1
            ):
                meaning_seq[seq_place] = potential_meaning

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
