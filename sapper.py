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
    """- ячейки"""

    count: int = Values.EMPTY.value

    def __init__(self, row, column):
        self.mine: bool = False  # мина или нет
        self.row: int = row  # номер строки
        self.column: int = column  # номер колонки
        self.id: int = Cells.get_id()  # порядковый номер
        self.count_mine: int = Values.EMPTY.value  # количество мин находящиеся рядом

    def __repr__(self):
        # return f"<{self.row}.{self.column}.{self.id}> <{self.mine}> <{self.count_mine}>"
        return f"<{self.mine}>"

    def set_mine(self):
        """- установить мину"""

        self.mine = True

    @staticmethod
    def get_id():
        """- получить идентификационный номер ячейки"""

        Cells.count += 1
        return Cells.count


class Field:
    """- поле"""

    def __init__(self):
        self.level: int = 0  # уровень сложности
        self.cells: list[list[Cells]] = []

    def set_difficulty(self, cxs: Type[Complex], st: str):
        """- установить значение уровня сложности"""

        for cx in cxs:
            if st == cx.name:
                self.level = cx.value
                break

    def create(self, horizon: range, vertical: range):
        """- создать матрицу 15X15"""

        lst = [
            [
                # добавляем объект ячейки в матрицу
                Cells(row=row, column=col)
                for col in vertical
            ]
            for row in horizon
        ]

        self.cells = lst

    def place_mines(self, size: int):
        """- расставить мины"""

        # получить список с id, уникальными идентификаторами объекта
        lst = [cl.id for cel in self.cells for cl in cel]

        # перемешать список с id рандомно
        random.shuffle(lst)

        # перезаписать матрицу, расставить мины,
        # используя перемешанный рандомно список и обрезанный по указателю сложности,
        # полученному от пользователя
        for cel in self.cells:
            for cl in cel:
                if cl.id in lst[: size]:
                    cl.set_mine()

    def fill_count_mine_nearby(self, grid: list, horizon: range, vertical: range, first: int, second: int, mine: int, ratio: int):
        """- заполнить матрицу количеством мин по соседству"""

        # создать индексы строк и столбцов для обхода матрицы
        for rows in horizon:
            for columns in vertical:

                # найти мину, для добавления значений соседним ячейкам
                if self.cells[rows][columns] == mine:

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
                            if self.cells[rows + row_dx][columns + col_dx] == mine:
                                continue

                            # если проверки проходят, то меняем значение в нашей матрице
                            self.cells[rows + row_dx][columns + col_dx] += ratio

    def init_field(self, str_level: str):
        """- инициализация данных клиента, сбор данных"""

        # установить уровень сложности
        self.set_difficulty(cxs=Complex, st=str_level)

        # создать матрицу
        self.create(
            horizon=range(Values.HORIZON.value),
            vertical=range(Values.VERTICAL.value)
        )

        # расставить мины
        self.place_mines(size=Values.SIZE.value)


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


if __name__ == '__main__':

    mx = Field()
    mx.init_field("EASY")

    for cell in mx.cells:
        # for cl in cell:
        print(cell)

    print("=" * 50)



    # print(mx.place_mines())

    # for cell in mx.cells:
    #     for cl in cell:
    #         print(cl.count)


