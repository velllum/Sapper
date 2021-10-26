import operator
import random

from enum import Enum
from typing import Type


class Complex(int, Enum):
    """- сложность"""

    EASY = 17
    MEDIUM = 30
    HARD = 45


class Values(int, Enum):
    """- Значение ячеек поля"""

    EMPTY = 0
    MINE = 9
    SIZE = 15
    RATIO = 1

    VERTICAL = SIZE
    HORIZON = SIZE
    FIELD = VERTICAL * HORIZON
    FIRST_INDEX = SIZE - SIZE
    SECOND_INDEX = SIZE - RATIO

    @staticmethod
    def GRID():
        return [-1, 0, 1]


class Cells:
    """- игрок, клиент, инициализация данных, оперирование данными"""

    count = Values.EMPTY.value

    def __init__(self, row, column):
        self.mine: bool = False  # мина или нет
        self.row: int = row  # номер строки
        self.column: int = column  # номер колонки
        self.number: int = Cells.get_number()  # порядковый номер
        self.count_near_mine: int = 0  # количество мин находящиеся рядом

    def __repr__(self):
        return f"<{self.row}.{self.column}.{self.number}> <{self.mine}>"

    @staticmethod
    def get_number():
        Cells.count += 1
        return Cells.count


class Field:
    """- реализация заполнения матрицы"""

    def __init__(self):
        self.level: int = 0  # уровень сложности
        self.field: list[list[int]] = []

    def set_difficulty(self, cxs: Type[Complex], st: str):
        """- установить значение уровня сложности"""

        for cx in cxs:
            if st == cx.name:
                self.level = cx.value
                break

    def create(self, size: int):
        """- создать матрицу 15X15"""

        # получить вложенные списки по размеру равномерной матрицы 15X15
        lst = [
            [
                Cells(row=row, column=col)
                for col in range(size)
            ]
            for row in range(size)
        ]

        self.field = lst

    def fill(self, grid: list, horizon: range, vertical: range, first: int, second: int, mine: int, ratio: int):
        """- заполнить матрицу по диагонали сверху и снизу"""

        # создать индексы строк и столбцов для обхода матрицы
        for rows in horizon:
            for columns in vertical:

                # найти мину, для добавления значений соседним ячейкам
                if self.field[rows][columns] == mine:

                    # обходим соседние ячейки, используя значения из списка [-1, 0, 1]
                    for row_dx in grid:
                        for col_dx in grid:

                            # получить переменные для проверки границ матрицы
                            rw = operator.add(rows, row_dx)
                            cl = operator.add(columns, col_dx)

                            # проверяем границы матрицы, если значения не существует то пропускаем
                            if cl < first or cl > second or rw < first or rw > second:
                                continue

                            if columns < first or columns > second or rows < first or rows > second:
                                continue

                            # проверяем значение в соседних ячейках на мины, при положительном результате пропускаем
                            if self.field[rows + row_dx][columns + col_dx] == mine:
                                continue

                            # если проверки проходят, то меняем значение в нашей матрице
                            self.field[rows + row_dx][columns + col_dx] += ratio

    def init_field(self, str_level: str):
        """- инициализация данных клиента, сбор данных"""
        # установить уровень сложности
        self.set_difficulty(cxs=Complex, st=str_level)

        # создать матрицу
        self.create(size=Values.SIZE.value)


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

    mx = Field()
    mx.init_field("EASY")

    for mx in mx.field:
        print(mx)

    # cl = Cells(1, 2)
    # print(cl)


