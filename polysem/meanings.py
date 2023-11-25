import csv
import os
import re
import weakref
from typing import Any, List, Sequence, Union

from polysem.settings import RESOURCE_PATH


def to_csv_array(obj: Any):
    return obj.__to_csv_array__()


class Meaning:
    instances: List = []

    def __init__(self, meaning_id: int, text: str, example: str) -> None:
        self.__class__.instances.append(weakref.proxy(self))
        self.id = meaning_id
        self.text = text
        self.example = example

    def __eq__(self, other: Any):
        if isinstance(other, Meaning):
            return self.__dict__ == other.__dict__
        return False

    def __repr__(self):
        return f"Meaning: {self.text}"

    def __str__(self):
        return self.__repr__()


class MeaningSign:
    def __init__(
        self,
        stem: str,
        semantics: str,
        meaning: Meaning,
        right_pos: Union[int, None, Sequence[int]] = None,
        left_pos: Union[int, None, Sequence[int]] = None,
    ) -> None:
        self.stem = stem
        self.semantics = semantics
        self.right_pos = right_pos
        self.left_pos = left_pos
        self.meaning = meaning

    def __eq__(self, other: Any):
        if isinstance(other, MeaningSign):
            return self.__dict__ == other.__dict__
        elif type(other) == str:
            return self.stem == other.strip().lower()
        return False

    def __repr__(self):
        return f"MeaningSign: {self.__dict__}"

    def __str__(self):
        return self.__repr__()

    def __to_csv_array__(self):
        left_pos = "-"
        right_pos = "-"

        if self.left_pos:
            left_pos = (
                f"{self.left_pos[0]}, {self.left_pos[1]}"
                if type(self.left_pos) in (list, tuple)
                else self.left_pos
            )

        if self.right_pos:
            right_pos = (
                f"{self.right_pos[0]}, {self.right_pos[1]}"
                if type(self.right_pos) in (list, tuple)
                else self.right_pos
            )

        return (
            self.stem,
            self.semantics,
            self.meaning.id,
            left_pos,
            right_pos,
        )


MeaningSeq = Sequence[Union[str, None, MeaningSign]]
MEANING_SEQ_SIDE = 5
MEANING_SEQ_MAX_SIZE = 1 + MEANING_SEQ_SIDE * 2


MEANING_1 = Meaning(
    1,
    "Имеющий температуру, сопоставимую с температурой человеческого тела; не очень горячий",
    "Против ожидания, вечер был так тих и тёпел, что свечи на террасе и в столовой горели неподвижными огнями",
)
MEANING_2 = Meaning(
    2,
    "Отапливаемый, нагретый до комфортного уровня",
    "Изменится ли угол α, если диск перенести из холодного помещения в теплое?",
)
MEANING_3 = Meaning(
    3,
    "Хорошо сохраняющий тепло, греющий",
    "Как это ни странно, для серьезного нарушения кровообращения достаточно промокших ног и не слишком теплой шапки",
)
MEANING_4 = Meaning(
    4,
    "Дающий внутреннее ощущение теплоты, согревающий душу",
    "Видимо, так происходит из-за теплого отношения автора к родному городу и его истории",
)
MEANING_5 = Meaning(
    5,
    "Доброжелательный, ласковый, участливый",
    "Тёплый приём",
)

MEANING_SINGS = []

# region Write .csv
# with open(
#     os.path.join(RESOURCE_PATH, "data", "meaningsings.csv"), mode="w", encoding="utf-8-sig"
# ) as w_file:
#     file_writer = csv.writer(w_file, delimiter=";", lineterminator="\r")
#     file_writer.writerow(
#         ["Number", "Stem", "Semantics", "Meaning", "Left position", "Right position"]
#     )

#     for i, ms in enumerate(MEANING_SINGS):
#         file_writer.writerow([i + 1, *to_csv_array(ms)])
# endregion

# region Load .csv
with open(
    os.path.join(RESOURCE_PATH, "data", "meaningsings.csv"),
    mode="r",
    encoding="utf-8-sig",
) as w_file:
    file_reader = csv.reader(w_file, delimiter=";", lineterminator="\r")
    next(file_reader)

    for arr in file_reader:
        left_pos = None if arr[4].strip() in ("-", "") else arr[4]
        right_pos = None if arr[5].strip() in ("-", "") else arr[5]

        if left_pos:
            if re.match(r"\[\d+,\s*\d+\]", left_pos):
                num1, num2 = re.findall(r"\d+", left_pos)
                left_pos = (int(num1), int(num2))
            else:
                left_pos = int(left_pos)

        if right_pos:
            if re.match(r"\[\d+,\s*\d+\]", right_pos):
                num1, num2 = re.findall(r"\d+", right_pos)
                right_pos = (int(num1), int(num2))
            else:
                right_pos = int(right_pos)

        if not left_pos and not right_pos:
            continue

        meaning = None

        for meaning_instance in Meaning.instances:
            if meaning_instance.id == int(arr[3]):
                meaning = meaning_instance

        if not meaning:
            continue

        MEANING_SINGS.append(
            MeaningSign(arr[1], arr[2], meaning, left_pos=left_pos, right_pos=right_pos)
        )
# endregion
