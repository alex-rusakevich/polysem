from typing import Any, Sequence, Union

from .meanings import *


class MeaningSign:
    def __init__(
        self,
        lemma: str,
        semantics: str,
        meaning: Meaning,
        right_pos: Union[int, None, Sequence[int]] = None,
        left_pos: Union[int, None, Sequence[int]] = None,
    ) -> None:
        self.lemma = lemma
        self.semantics = semantics
        self.right_pos = right_pos
        self.left_pos = left_pos
        self.meaning = meaning

    def __eq__(self, other: Any):
        if isinstance(other, MeaningSign):
            return self.__dict__ == other.__dict__
        elif type(other) == str:
            return self.lemma == other.strip().lower()
        return False

    def __repr__(self):
        return f"MeaningSign: {self.__dict__}"

    def __str__(self):
        return self.__repr__()


MeaningSeq = Sequence[Union[str, None, MeaningSign]]
MEANING_SEQ_SIDE = 5
MEANING_SEQ_MAX_SIZE = 1 + MEANING_SEQ_SIDE * 2

MEANING_SINGS = (
    MeaningSign("свеча", "предмет, излучающий тепло", MEANING_1, right_pos=(1, 2)),
    MeaningSign("помещение", "пространство", MEANING_2, right_pos=1),
    MeaningSign("куртка", "предмет одежды", MEANING_3, right_pos=1),
    MeaningSign("цвет", "характеристика оптического диапазона", MEANING_4, right_pos=1),
    MeaningSign("прием", "разновидность встречи", MEANING_5, right_pos=1),
)
