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
    SIZE = 15
    RATIO = 1

    VERTICAL = SIZE
    HORIZON = SIZE
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
        return f"<{self.row}.{self.column}.{self.id}> <{self.mine}> <{self.count_mine}>"
        # return f"<{self.mine} {self.count_mine}>"

    def set_mine(self):
        """- установить мину"""
        self.mine = True

    def set_count_mine(self, ):
        """- увеличить кол. мин находящихся по соседству"""
        if not self.mine:
            self.count_mine += Values.RATIO.value

    @classmethod
    def get_id(cls):
        """- получить идентификационный номер ячейки"""
        cls.count += 1
        return cls.count


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

    def fill_count_mine_nearby(self, grid: list, first: int, second: int):
        """- заполнить матрицу объектов количеством мин по соседству"""
        # создать индексы строк и столбцов для обхода матрицы
        for cells in self.cells:
            for cs in cells:

                # найти мину, для добавления значений соседним ячейкам
                if not cs.mine:
                    continue

                # обходим соседние ячейки, используя значения из списка [-1, 0, 1]
                for row_dx in grid:
                    for col_dx in grid:

                        # получить переменные для проверки границ матрицы
                        rw = operator.add(cs.row, row_dx)
                        cl = operator.add(cs.column, col_dx)

                        # проверяем границы матрицы, если значения не существует то пропускаем
                        if cl < first or cl > second or rw < first or rw > second:
                            continue

                        if cs.column < first or cs.column > second or cs.row < first or cs.row > second:
                            continue

                        # если проверки проходят, то меняем значение в нашей матрице
                        self.cells[rw][cl].set_count_mine()

    def init_field(self, str_level: str):  # временно
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

        # делаем подсказки, указываем на количество мин по соседству
        self.fill_count_mine_nearby(
            grid=Values.GRID(),
            first=Values.FIRST_INDEX.value,
            second=Values.SECOND_INDEX.value,
        )


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



