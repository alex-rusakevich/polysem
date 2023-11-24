import weakref
from typing import Any, List, Sequence, Union


class Meaning:
    instances: List = []

    def __init__(self, text: str, example: str) -> None:
        self.__class__.instances.append(weakref.proxy(self))
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


MEANING_1 = Meaning(
    "Имеющий температуру, сопоставимую с температурой человеческого тела; не очень горячий",
    "Против ожидания, вечер был так тих и тёпел, что свечи на террасе и в столовой горели неподвижными огнями. А. И. Куприн, «Гранатовый браслет»",
)
MEANING_2 = Meaning("Отапливаемый, нагретый до комфортного уровня", "Тёплое помещение")
MEANING_3 = Meaning("Хорошо сохраняющий тепло, греющий", "Тёплая куртка")
MEANING_4 = Meaning(
    "Дающий внутреннее ощущение теплоты, согревающий душу",
    "Теплые стены родного дома",
)
MEANING_5 = Meaning(
    "Доброжелательный, ласковый, участливый",
    "Тёплый приём",
)


"""

Examples:

(2) 1. И вы выходите из своего теплого дома в холодное утро и идете навстречу другу, который тоже не хочет идти ловить рыбу.
(1) 2. Не волнуйся, замшевые перчатки можно стирать в теплой мыльной воде, надев их на руки.
(5) 3. Король Иордании, в свою очередь, заявил, что у отношения с Президентом России сложились очень теплые.
(4) 4. У меня сохранились теплые воспоминания о походах туда с бабушкой и родителями, катаниях на пони по кругу, мороженом, кормлении (украдкой — простите, сотрудники!) уток в прудах.
(2) 5. Изменится ли угол α, если диск перенести из холодного помещения в теплое?
(4) 6. Видимо, так происходит из-за теплого отношения автора к родному городу и его истории.
(5) 7. Выяснилось это позднее, когда он успел завести добрые отношения с несколькими симпатичными "красными " и, иронизируя над собой, говорил жене о теплой дружбе русского монархиста с кастильскими большевиками.
(3) 8. Как это ни странно, для серьезного нарушения кровообращения достаточно промокших ног и не слишком теплой шапки
(2) 9. Вот и теперь сидят они в теплой тени полуподвала русской церкви и, осененные православным крестом, пьют теплое красное вино.
(1) 10. И тут же, на теплых красных камнях, Марей греет губами прохладную, бледно-розовую морошку.
(1) 11. С трёх сторон, одновременно, отрезая все пути к отступлению,– только обрыв за спиной, где полусотней локтей ниже плещется о камни тёплое море. 
"""


MEANING_SINGS = (
    # region Meaning 1
    MeaningSign(
        "свеча",
        "предмет, излучающий тепло",
        MEANING_1,
        right_pos=(1, 2),
    ),
    MeaningSign(
        "вода",
        "субстанция, излучающая тепло",
        MEANING_1,
        right_pos=(1, 2),
    ),
    MeaningSign(
        "камень",
        "предмет, излучающий тепло",
        MEANING_1,
        right_pos=(1, 2),
    ),
    MeaningSign(
        "море",
        "жидкость, излучающая тепло",
        MEANING_1,
        right_pos=1,
    ),
    # endregion
    # region Meaning 2
    MeaningSign("помещение", "пространство", MEANING_2, right_pos=1, left_pos=2),
    MeaningSign(
        "дом",
        "пространство",
        MEANING_2,
        left_pos=1,
    ),
    MeaningSign(
        "полуподвал",
        "пространство",
        MEANING_2,
        right_pos=2,
    ),
    # endregion
    # region Meaning 3
    MeaningSign("куртка", "предмет одежды", MEANING_3, right_pos=1),
    MeaningSign("шапка", "предмет одежды", MEANING_3, right_pos=(1, 3)),
    # endregion
    # region Meaning 4
    MeaningSign(
        "родной",
        "характеристика отношения к человеку",
        MEANING_4,
        right_pos=1,
    ),
    MeaningSign(
        "отношение",
        "мнение человека",
        MEANING_4,
        right_pos=1,
    ),
    MeaningSign(
        "воспоминание",
        "образ в памяти",
        MEANING_4,
        right_pos=1,
    ),
    # endregion
    # region Meaning 5
    MeaningSign(
        "прием",
        "разновидность встречи",
        MEANING_5,
        right_pos=1,
    ),
    MeaningSign(
        "президент",
        "высшая должность в государстве",
        MEANING_5,
        left_pos=4,
    ),
    MeaningSign(
        "складываться",
        "созидательное действие",
        MEANING_5,
        left_pos=(1, 3),
    ),
    MeaningSign(
        "дружба",
        "вид взаимоотношений между людьми",
        MEANING_5,
        right_pos=1,
    ),
    # endregion
)
