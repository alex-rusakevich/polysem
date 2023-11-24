import weakref
from typing import Any, List


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


MEANING_1 = Meaning(
    "Имеющий температуру, сопоставимую с температурой человеческого тела; не очень горячий",
    "Против ожидания, вечер был так тих и тёпел, что свечи на террасе и в столовой горели неподвижными огнями. А. И. Куприн, «Гранатовый браслет»",
)
MEANING_2 = Meaning("Отапливаемый, нагретый до комфортного уровня", "Тёплое помещение")
MEANING_3 = Meaning("Хорошо сохраняющий тепло, греющий", "Тёплая куртка")
MEANING_4 = Meaning(
    "Имеющий цветовой оттенок, вызывающий ассоциации с огнём",
    "Стены комнаты были выкрашены в теплые цвета",
)
MEANING_5 = Meaning(
    "Доброжелательный, ласковый, участливый",
    "Тёплый приём",
)
