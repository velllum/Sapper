import json
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
    def GRID() -> list:
        """- список с значениями для обхода ячеек"""
        return [-1, 0, 1]

    @staticmethod
    def DEFAULT_BOOL() -> bool:
        """- значение по умолчанию мины"""
        return False


class Cell(object):
    """- ячейки"""

    count: int = Values.EMPTY.value

    def __init__(self, row, column):
        self.is_mine: bool = Values.DEFAULT_BOOL()  # ячейка мина или нет
        self.is_hidden: bool = Values.DEFAULT_BOOL()  # ячейка скрыто или нет
        self.row: int = row  # номер строки
        self.column: int = column  # номер колонки
        self.id: int = Cell.get_id()  # порядковый номер
        self.count_mine_near: int = Values.EMPTY.value  # количество мин находящиеся рядом

    def set_mine(self):
        """- установить мину"""
        self.is_mine = True

    def set_count_mine(self):
        """- увеличить кол. мин находящихся по соседству"""
        if not self.is_mine:
            self.count_mine_near += Values.RATIO.value

    def get_coord(self) -> json:
        """- поучить координаты для матрицы, номера строки и колонки"""
        return json.dumps(dict(rw=self.row, cl=self.column))

    @classmethod
    def get_id(cls) -> int:
        """- получить идентификационный номер ячейки"""
        cls.count += Values.RATIO.value
        return cls.count

    def __repr__(self):
        # return f"<{self.row}.{self.column}.{self.id}> <{self.is_mine}> <{self.count_mine}>"
        return f"<{self.is_mine} {self.count_mine_near} {self.is_hidden}>"


class Field(object):
    """- поле"""

    def __init__(self):
        self.cells: list[list[Cell]] = []
        self.count_mine_field: int = Values.EMPTY.value  # уровень сложности, по умолчанью ноль

    def get_cell(self, rw: int, cl: int) -> Cell:
        """- получить ячейку по значениям столбца и строки"""
        return self.cells[rw][cl]

    def set_difficulty(self, st: str):
        """- установить значение уровня сложности"""
        for cx in Complex:
            if st == cx.name:
                self.count_mine_field = cx.value
                break

    def create(self, cl: Type[Cell]):
        """- создать матрицу 15X15"""

        lst = [
            [
                # добавляем объект ячейки в матрицу
                cl(row=row, column=col)
                for col in range(Values.VERTICAL.value)
            ]
            for row in range(Values.HORIZON.value)
        ]

        self.cells = lst

    def place_mines(self):
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
                if cl.id in lst[: self.count_mine_field]:
                    cl.set_mine()

    def fill_count_mine_nearby(self):
        """- заполнить матрицу объектов количеством мин по соседству"""

        grid: list = Values.GRID()
        first: int = Values.FIRST_INDEX.value
        second: int = Values.SECOND_INDEX.value

        # создать индексы строк и столбцов для обхода матрицы
        for cells in self.cells:
            for cs in cells:

                # найти мину, для добавления значений соседним ячейкам
                if not cs.is_mine:
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


class Game(object):
    """- уровень игры, варианты окончание игры, победа, поражение, начало игры, конец игры"""

    cell: Type[Cell] = Cell

    def __init__(self):
        self.field: Field = Field()

    def start(self, level: str):
        """- начало игры"""

        # получаем уровень сложности, выбранный пользователем и устанавливаем какое будет количество мин на поле
        self.field.set_difficulty(st=level)

        # создать матрицу
        self.field.create(cl=Game.cell)

        # расставить мины
        self.field.place_mines()

        # делаем подсказки, указываем на количество мин по соседству
        self.field.fill_count_mine_nearby()

    def defeats(self, **kwargs):
        """- поражения в игре"""

        # TODO логика: поражение в игре происходит когда клиент открыл ячейку с миной
        #  Получает объект от интерфейса игры, и проверяет не является ли объект миной,
        #  если да то игра считается проигранной

        # получить ячейку по значению строки и колонки
        cell = self.field.get_cell(**kwargs)

        # проверка на поражение в игре, если пользователь столкнулся с миной
        if cell.is_mine is not Values.DEFAULT_BOOL():
            return True

        return False

    def victory(self):
        """- победа в игре"""
        # TODO: победа в игре происходит когда открыты все ячейки, и не открыты ячейки с минами

    def end(self):
        """- конец игры"""
        # TODO: конец игры происходит когда клиент закрыл игру, покинул сервер

# if __name__ == '__main__':
#
#     # Client - реализация действий клиента
#
#     gm = Game()
#
#     gm.start(level="EASY")
#
#     print("=" * 50)
#
#     for cell in gm.field.cells:
#         print(cell)
#
#     print("=" * 50)
