import random

from enum import Enum
from typing import Type


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

    def __init__(self):
        self.level: int = 0  # уровень сложности
        self.data: list[int] = []
        self.matrix: list[list[int]] = []

    def set_difficulty(self, complex: Type[Complex], st: str):
        """- установить значение уровня сложности"""

        for comp in complex:
            if st == comp.name:
                self.level = comp.value
                break

    def create_data(self, cell_empty: int, cell_field: int, cell_mine: int):
        """- создать список с метками мин и пустых ячеек, перемешать рандомно"""

        # собрать в список значение 0 - пустое, 9 - мина
        lst = [
            *[cell_empty] * (cell_field - self.level),
            *[cell_mine] * self.level
        ]

        # перемешать список рандомно
        random.shuffle(lst)

        self.data = lst

    def create_matrix(self, cell_field: int, cell_num: int):
        """- создать матрицу 15X15"""

        # получить вложенные списки по размеру равномерной матрицы 15X15
        lst = [
            self.data[cl: cl + cell_num]
            for cl in range(0, cell_field, cell_num)
        ]

        self.matrix = lst

    def select_cells(self):
        """- поднять значение ячейки, если рядом есть мины"""


    def init_client(self, str_level: str):
        """- инициализация данных клиента, сбор данных"""

        # установить уровень сложности
        self.set_difficulty(
            complex=Complex,
            st=str_level,
        )

        # создать перемешанный список пустых и значений с установки мин
        self.create_data(
            cell_empty=Cells.EMPTY.value,
            cell_field=Cells.FIELD.value,
            cell_mine=Cells.MINE.value,
        )

        # создать матрицу
        self.create_matrix(
            cell_field=Cells.FIELD.value,
            cell_num=Cells.NUM.value,
        )


class Field:
    """- игровое поле, заполнение поля, проверка на поле ..., выявление на поле ..., операции с ячейками"""

    def __init__(self):
        self.client = Client()

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

    lst = [
        *[Cells.EMPTY.value] * (Cells.FIELD - Complex.EASY),
        *[Cells.MINE.value] * Complex.EASY
    ]

    random.shuffle(lst)

    cls = [
        lst[cell: cell + Cells.NUM]
        for cell in range(0, Cells.FIELD, Cells.NUM)
    ]

    for row in range(Cells.NUM.value):

        # print(cls[row])

        for col in range(Cells.NUM.value):

            if cls[row][col] == Cells.MINE.value:

                if not col == (15 - 1) and cls[row][col + 1] != 9:
                    cls[row][col + 1] = cls[row][col + 1] + 1

                if not col == 0 and cls[row][col - 1] != 9:
                    cls[row][col - 1] = cls[row][col - 1] + 1

                if not row == 0 and cls[row - 1][col] != 9:
                    cls[row - 1][col] = cls[row - 1][col] + 1

                if not row == (15 - 1) and cls[row + 1][col] != 9:
                    cls[row + 1][col] = cls[row + 1][col] + 1

    for i in cls:
        print(i)


