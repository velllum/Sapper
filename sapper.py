import random

from enum import Enum

#  простой уровень - 10 бомб, (10% от 100%)
#  простой средний уровень - 20 бомб, (20% от 100%)
#  простой сложный уровень - 30 бомб, (30% от 100%)


class Const(int, Enum):
    """- константы"""

    EASY = 15
    MEDIUM = 30
    HARD = 45

    NUM_CELLS = 15
    VERTIC_CELLS = NUM_CELLS
    HORIZON_CELLS = NUM_CELLS
    FIELD_CELLS = VERTIC_CELLS * HORIZON_CELLS


class Client:
    """- игрок, клиент, инициализация данных, оперирование данными"""

    def __init__(self, level, app):
        self.level = level  # уровень сложности
        self.app = app

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

    def number_mine(self):
        """- количество мин на поле"""


class Game:
    """- уровень игры, варианты окончание игры, победа, поражение, начало игры, конец игры"""

    def start(self):
        """- начало игры"""

    def end(self):
        """- конец игры"""

    def victory(self):
        """- победа в игре"""

    def defeats(self):
        """- поражения в игре"""


class Manager:
    """- точка входа"""


if __name__ == '__main__':

    print("=" * 50)

    lst = [
        *[0] * (Const.FIELD_CELLS - Const.EASY),
        *[1] * Const.EASY
    ]

    random.shuffle(lst)

    print(lst)

    lst_cells = list(range(Const.FIELD_CELLS))

    print("=" * 100)

    lst_field = [
        lst[cell: cell + Const.NUM_CELLS]
        for cell in range(0, Const.FIELD_CELLS, Const.NUM_CELLS)
    ]

    for i in lst_field:
        print(i, len(i))





