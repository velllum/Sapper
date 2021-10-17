import random

from enum import Enum

#  простой уровень - 10 бомб, (10% от 100%)
#  простой средний уровень - 20 бомб, (20% от 100%)
#  простой сложный уровень - 30 бомб, (30% от 100%)


class GameEnum(Enum):
    """- константы"""
    level_one = 10
    level_two = 20
    level_three = 30


class Client:
    """- игрок, клиент, инициализация данных, оперирование данными"""

    def __init__(self, level):
        self.level = level  # уровень сложности

    def get_number_mine(self):
        """- получить количество мин на поле"""

    def generate_data(self):
        """- сгенерировать матрицу с данными"""


class Field:
    """- игровое поле, заполнение поля, проверка на поле ..., выявление на поле ..., операции с ячейками"""

    def vertical(self, field):
        """- проверка по вертикали"""

    def horizontal(self, field):
        """- проверка по горизонтали"""

    def diagonal(self, field):
        """- проверка по диагонали"""


class Game:
    """- уровень игры, варианты окончание игры, победа, поражение, """


class Manager:
    """- точка входа, начало игры, конец игры"""


if __name__ == '__main__':

    print("=" * 50)

    lst = [*[0] * 90, *[1] * 10]
    random.shuffle(lst)

    for e, i in enumerate(lst):

        if e % 10 == 0 and e != 0:
            print("\r")

        print(" ", i, " ", end="")

    print("\r")
    print("=" * 50)




