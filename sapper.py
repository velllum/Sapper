import operator
import random

from enum import Enum
from typing import Type


class Complex(int, Enum):
    """- сложность"""

    EASY = 17
    MEDIUM = 30
    HARD = 45


class Cells(int, Enum):
    """- ячейки поля"""

    EMPTY = 0
    MINE = 9
    SIZE = 15
    RATIO = 1

    VERTICAL = SIZE
    HORIZON = SIZE
    FIELD = VERTICAL * HORIZON
    FIRST_INDEX = SIZE - RATIO
    SECOND_INDEX = SIZE - SIZE


class Matrix:
    """- реализация заполнения матрицы"""

    def __init__(self):
        self.matrix: list[list[int]] = []

        self.mine: int = Cells.MINE.value
        self.ratio: int = Cells.RATIO.value

    def create_matrix(self, dt: list[int], field: int, size: int):
        """- создать матрицу 15X15"""

        # получить вложенные списки по размеру равномерной матрицы 15X15
        matrix = [
            dt[cl: cl + size]
            for cl in range(0, field, size)
        ]

        self.matrix = matrix

    def fill_horizontal(self, position: operator, rows: int, columns: int, ind: int):
        """- заполнить матрицу по горизонтали слева и справа"""

        # проверка, если значение первое или последнее (чтоб не оперировать в матрице с не существующими значениями)
        # и если оно не равно значению мины, тогда выполнить операцию
        if columns != ind and self.matrix[rows][position] != self.mine:
            self.matrix[rows][position] += self.ratio

    def fill_vertically(self, position: operator, rows: int, columns: int, ind: int):
        """- заполнить матрицу по вертикали сверху и снизу"""

        # проверка, если значение первое или последнее (чтоб не оперировать в матрице не существующими значениями)
        # и если оно не равно значению мины, тогда выполнить операцию
        if rows != ind and self.matrix[position][columns] != self.mine:
            self.matrix[position][columns] += self.ratio

    def fill_diagonally(self, row_pos: operator, col_pos: operator, rows: int, columns: int, sd_ind: int, ft_ind: int):
        """- заполнить матрицу по диагонали сверху и снизу"""

        # проверка, если значение первое или последнее (чтоб не оперировать в матрице не существующими значениями)
        # и если оно не равно значению мины, тогда выполнить операцию
        if rows != sd_ind and columns != ft_ind and self.matrix[row_pos][col_pos] != self.mine:
            self.matrix[row_pos][col_pos] += self.ratio

    def init_matrix(self, cells: Type[Cells], lst: list[int], horizon: range, vertical: range):
        """- заполнить матрицу, данными подсказок расположение мин"""

        self.create_matrix(
            dt=lst,
            field=cells.FIELD.value,
            size=cells.SIZE.value,
        )

        for rows in horizon:

            for columns in vertical:

                if self.matrix[rows][columns] == self.mine:

                    kwargs = dict(
                        rows=rows,
                        columns=columns,
                    )

                    """заполнить матрицу по горизонтали"""
                    # слева
                    self.fill_horizontal(
                        position=operator.sub(columns, self.ratio),
                        ind=cells.SECOND_INDEX.value,
                        **kwargs,
                    )

                    # справа
                    self.fill_horizontal(
                        position=operator.add(columns, self.ratio),
                        ind=cells.FIRST_INDEX.value,
                        **kwargs,
                    )

                    """по вертикали"""
                    # снизу
                    self.fill_vertically(
                        position=operator.add(rows, self.ratio),
                        ind=cells.FIRST_INDEX.value,
                        **kwargs,
                    )

                    # сверху
                    self.fill_vertically(
                        position=operator.sub(rows, self.ratio),
                        ind=cells.SECOND_INDEX.value,
                        **kwargs,
                    )

                    """по диагонали"""
                    # сверху справа
                    self.fill_diagonally(
                        row_pos=operator.sub(rows, self.ratio),
                        col_pos=operator.add(columns, self.ratio),
                        ft_ind=cells.FIRST_INDEX.value,
                        sd_ind=cells.SECOND_INDEX.value,
                        **kwargs,
                    )

                    # сверху слева
                    self.fill_diagonally(
                        row_pos=operator.sub(rows, self.ratio),
                        col_pos=operator.sub(columns, self.ratio),
                        ft_ind=cells.SECOND_INDEX.value,
                        sd_ind=cells.SECOND_INDEX.value,
                        **kwargs,
                    )

                    # снизу справа
                    self.fill_diagonally(
                        row_pos=operator.add(rows, self.ratio),
                        col_pos=operator.add(columns, self.ratio),
                        ft_ind=cells.FIRST_INDEX.value,
                        sd_ind=cells.FIRST_INDEX.value,
                        **kwargs,
                    )

                    # снизу слева
                    self.fill_diagonally(
                        row_pos=operator.add(rows, self.ratio),
                        col_pos=operator.sub(columns, self.ratio),
                        ft_ind=cells.SECOND_INDEX.value,
                        sd_ind=cells.FIRST_INDEX.value,
                        **kwargs,
                    )


class Data:
    """- игрок, клиент, инициализация данных, оперирование данными"""

    def __init__(self):
        self.level: int = 0  # уровень сложности
        self.data: list[int] = []
        self.mx = Matrix()

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

    def init_data(self, str_level: str):
        """- инициализация данных клиента, сбор данных"""

        # установить уровень сложности
        self.set_difficulty(
            cxs=Complex,
            st=str_level,
        )

        # создать перемешанный список пустых значений и значений мин
        self.create_data(
            empty=Cells.EMPTY.value,
            field=Cells.FIELD.value,
            mine=Cells.MINE.value,
        )

        # инициализация и создание матрицы
        self.mx.init_matrix(
            cells=Cells,
            lst=self.data,
            horizon=range(Cells.HORIZON.value),
            vertical=range(Cells.VERTICAL.value),
        )


class Field:
    """- игровое поле, заполнение поля, проверка на поле ..., выявление на поле ..., операции с ячейками"""

    def __init__(self):
        self.client = Data()

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

    data = Data()
    data.init_data("EASY")

    for mx in data.mx.matrix:
        print(mx)

    # lst = [
    #     *[Cells.EMPTY.value] * (Cells.FIELD - Complex.EASY),
    #     *[Cells.MINE.value] * Complex.EASY
    # ]
    #
    # random.shuffle(lst)
    #
    # cls = [
    #     lst[cell: cell + Cells.SIZE]
    #     for cell in range(0, Cells.FIELD, Cells.SIZE)
    # ]
    #
    # for row in range(Cells.SIZE.value):
    #
    #     # print(cls[row])
    #
    #     for col in range(Cells.SIZE.value):
    #
    #         if cls[row][col] == Cells.MINE.value:
    #
    #             # по горизонтали
    #             if col != (15 - 1) and cls[row][col + 1] != 9:
    #                 cls[row][col + 1] += 1
    #
    #             if col != 0 and cls[row][col - 1] != 9:
    #                 cls[row][col - 1] += 1
    #
    #             # по вертикали
    #             if row != 0 and cls[row - 1][col] != 9:
    #                 cls[row - 1][col] += 1
    #
    #             if row != (15 - 1) and cls[row + 1][col] != 9:
    #                 cls[row + 1][col] += 1
    #
    #             """по диагонали"""
    #             # сверху справа
    #             if row != 0 and col != (15 - 1) and cls[row - 1][col + 1] != 9:
    #                 cls[row - 1][col + 1] += 1
    #
    #             # сверху слева
    #             if row != 0 and col != 0 and cls[row - 1][col - 1] != 9:
    #                 cls[row - 1][col - 1] += 1
    #
    #             # снизу справа
    #             if row != (15 - 1) and col != (15 - 1) and cls[row + 1][col + 1] != 9:
    #                 cls[row + 1][col + 1] += 1
    #
    #             # снизу слева
    #             if row != (15 - 1) and col != 0 and cls[row + 1][col - 1] != 9:
    #                 cls[row + 1][col - 1] += 1
    #
    # for i in cls:
    #     print(i)


