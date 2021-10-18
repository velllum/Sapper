import random

from enum import Enum


class Complex(int, Enum):
    """- сложность"""

    EASY = 15
    MEDIUM = 30
    HARD = 45


class Cells(int, Enum):
    """- ячейки поля"""

    EMPTY = 0
    MINE = 9
    NUM = 15
    VERTICAL = NUM
    HORIZON = NUM
    FIELD = VERTICAL * HORIZON


class Client:
    """- игрок, клиент, инициализация данных, оперирование данными"""

    def __init__(self, level, app):
        self.level = level  # уровень сложности
        self.app = app  # объект Flask

    def set_difficulty_level(self, string: str):
        """- установить уровень сложности"""

        if string == "easy":
            self.level = Complex.EASY.value

        elif string == "medium":
            self.level = Complex.MEDIUM.value

        elif string == "hard":
            self.level = Complex.HARD.value

    def generate_data(self):
        """- сгенерировать матрицу с данными"""

        # собрать в общий список значение 0 - пустое, 9 - мина
        lst = [
            *[Cells.EMPTY.value] * (Cells.FIELD - self.level),
            *[Cells.MINE.value] * self.level
        ]

        # перемешать список рандомно
        random.shuffle(lst)

        # получить вложенные списки по размеру равномерной матрицы
        lst_field = [
            lst[cell: cell + Cells.NUM]
            for cell in range(0, Cells.FIELD, Cells.NUM)
        ]

        return lst_field


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

    print(Cells.MINE.value)

    lst = [
        *[Cells.EMPTY.value] * (Cells.FIELD - Complex.EASY),
        *[Cells.MINE.value] * Complex.EASY
    ]

    random.shuffle(lst)

    lst_field = [
        lst[cell: cell + Cells.NUM]
        for cell in range(0, Cells.FIELD, Cells.NUM)
    ]

    for i in lst_field:
        print(i, len(i))
