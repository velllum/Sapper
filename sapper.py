import operator
import random

from enum import Enum
from typing import Type, Any


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


class Matrix:
    """- реализация заполнения матрицы"""

    def __init__(self):
        self.level: int = 0  # уровень сложности
        self.data: list[int] = []
        self.matrix: list[list[int]] = []

    def set_difficulty(self, cxs: Type[Complex], st: str):
        """- установить значение уровня сложности"""

        for cx in cxs:
            if st == cx.name:
                self.level = cx.value
                break

    def create_data(self, empty: int, field: int, mine: int):
        """- создать список с метками мин и пустых ячеек, перемешать рандомно"""

        # собрать в список значение 0 - пустое, 9 - мина
        lst = [
            *[empty] * (field - self.level),
            *[mine] * self.level
        ]

        # перемешать список рандомно
        random.shuffle(lst)

        self.data = lst

    def create_matrix(self, field: int, size: int):
        """- создать матрицу 15X15"""

        # получить вложенные списки по размеру равномерной матрицы 15X15
        matrix = [
            self.data[cl: cl + size]
            for cl in range(0, field, size)
        ]

        self.matrix = matrix

    def fill_matrix(self, grid: list, horizon: range, vertical: range, first: int, second: int, mine: int, ratio: int):
        """- заполнить матрицу по диагонали сверху и снизу"""

        # создать индексы строк и столбцов для обхода матрицы
        for rows in horizon:
            for columns in vertical:

                # найти мину, для добавления значений соседним ячейкам
                if self.matrix[rows][columns] == mine:

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
                            if self.matrix[rows + row_dx][columns + col_dx] == mine:
                                continue

                            # если проверки проходят, то меняем значение в нашей матрице
                            self.matrix[rows + row_dx][columns + col_dx] += ratio

    def init_matrix(self, str_level: str):
        """- инициализация данных клиента, сбор данных"""
        # установить уровень сложности
        self.set_difficulty(
            cxs=Complex,
            st=str_level,
        )

        # создать перемешанный список пустых значений и значений мин
        self.create_data(
            empty=Values.EMPTY.value,
            field=Values.FIELD.value,
            mine=Values.MINE.value,
        )

        # создать матрицу
        self.create_matrix(
            field=Values.FIELD.value,
            size=Values.SIZE.value,
        )

        # заполнить матрицу, данными подсказок расположение мин
        self.fill_matrix(
            grid=Values.GRID(),
            horizon=range(Values.HORIZON.value),
            vertical=range(Values.VERTICAL.value),
            first=Values.FIRST_INDEX.value,
            second=Values.SECOND_INDEX.value,
            mine=Values.MINE.value,
            ratio=Values.RATIO.value,
        )


class Cells:
    """- игрок, клиент, инициализация данных, оперирование данными"""

    def __init__(self, row, column, number, count_near_mine):
        self.mine: bool = False
        self.row: int = row
        self.column: int = column
        self.number: int = number
        self.count_near_mine: int = count_near_mine

    def __repr__(self):
        return f"Cell ind-<{self.row}.{self.column}> | mine-<{self.mine}>"


class Field:
    """- игровое поле, заполнение поля, проверка на поле ..., выявление на поле ..., операции с ячейками"""

    def __init__(self):
        pass

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

    mx = Matrix()
    mx.init_matrix("EASY")

    for mx in mx.matrix:
        print(mx)

    cl = Cells(1, 2)
    print(cl)


