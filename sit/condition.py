from enum import Enum


class Condition(Enum):

    def __new__(cls, *args, **kwargs):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, text: str, background_color: str, text_color: str, int_value: int):
        self.text = text
        self.background_color = background_color
        self.text_color = text_color
        self.int_value = int_value

    ONE   = 'Poor',      '#9e2121', 'white', 1
    TWO   = 'Fair',      '#636363', 'white', 2
    THREE = 'Good',      '#3d37bd', 'white', 3
    FOUR  = 'Excellent', '#35a147', 'white', 4

    @staticmethod
    def get_by_value(value: int):
        if value == 1:
            return Condition.ONE
        elif value == 2:
            return Condition.TWO
        elif value == 3:
            return Condition.THREE
        elif value == 4:
            return Condition.FOUR
        else:
            raise Exception(f'No such condition - {value}')
