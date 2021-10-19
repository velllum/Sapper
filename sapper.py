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
        self.level: int  # уровень сложности
        self.matrix: list[list[int]]

    def set_difficulty(self, comp: Type[Complex], st: str):
        """- установить значение уровня сложности"""

        if st == comp.EASY.name:
            self.level = comp.EASY.value

        elif st == comp.MEDIUM.name:
            self.level = comp.MEDIUM.value

        elif st == comp.HARD.name:
            self.level = comp.HARD.value

    def create_data(self, cell: Type[Cells]) -> list[int]:
        """- создать список с метками мин и пустых ячеек, перемешать рандомно"""

        # собрать в список значение 0 - пустое, 9 - мина
        lst = [
            *[cell.EMPTY.value] * (cell.FIELD.value - self.level),
            *[cell.MINE.value] * self.level
        ]

        # перемешать список рандомно
        random.shuffle(lst)

        return lst

    def create_matrix(self, cell: Type[Cells], lst: list) -> list[list[int]]:
        """- создать матрицу 15X15"""

        # получить вложенные списки по размеру равномерной матрицы 15/15
        return [
            lst[cl: cl + cell.NUM.value]
            for cl in range(0, cell.FIELD.value, cell.NUM.value)
        ]

    def select_cells(self):
        """- выделить ячейки, указав количество рядом находящихся мин, если есть близ мина"""

    def init_client(self, str_level: str):
        """- инициализация данных клиента, сбор данных"""

        # установить уровень сложности
        self.set_difficulty(
            comp=Complex,
            st=str_level
        )

        # создать перемешанный список пустых и значений с данными растоновки мин
        data = self.create_data(
            cell=Cells,
        )

        # создать матрицу
        matrix = self.create_matrix(
            cell=Cells,
            lst=data
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


