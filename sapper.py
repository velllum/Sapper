import operator
import random

from enum import Enum
from typing import Type, List, Union, Tuple

from flask import request


class Complex(int, Enum):
    """- сложность"""

    EASY = 30
    MEDIUM = 40
    HARD = 50


class Values(int, Enum):
    """- Значение ячеек поля"""

    EMPTY = 0
    SIZE = 15
    RATIO = 1

    VERTICAL = SIZE
    HORIZON = SIZE
    FIRST_INDEX = SIZE - SIZE
    SECOND_INDEX = SIZE - RATIO
    FULL_CELLS = VERTICAL * HORIZON

    @staticmethod
    def grid() -> List[int]:
        """- список с значениями для обхода ячеек
        по вертикали, горизонтали и диагонали"""
        return [-1, 0, 1]


class Cell(object):
    """- ячейки"""

    count_id: int = Values.EMPTY.value
    count_open_cells: int = Values.EMPTY.value

    def __init__(self, row, column):
        self.is_mine: bool = False  # ячейка мина или нет
        self.is_open: bool = False  # ячейка скрыто или нет
        self.row: int = row  # номер строки
        self.column: int = column  # номер колонки
        self.id: int = Cell.create_id()  # порядковый номер
        self.count_mine_near: int = Values.EMPTY.value  # количество мин находящиеся рядом
        self.open_cells: int = Values.EMPTY.value  # количество открытых ячеек, по умолчанию ноль

    def set_count_mine(self):
        """- увеличить кол. мин находящихся по соседству"""
        if not self.is_mine:
            self.count_mine_near += Values.RATIO.value

    def set_mine(self):
        """- установить мину"""
        self.is_mine = True

    def set_open(self):
        """- установить ячейку из скрытой в открытую"""
        # счетчик подсчета количества открытых ячеек
        if self.is_open is not True:
            Cell.set_count_open_cells()
        self.is_open = True

    def is_count_mine(self):
        """- проверка если значение больше ноля, то True"""
        if self.count_mine_near != Values.EMPTY.value:
            return True
        return False

    @classmethod
    def get_count_open_cells(cls):
        return cls.count_open_cells

    @classmethod
    def set_count_open_cells(cls):
        """- увеличить количество ячеек, которые были открыты"""
        cls.count_open_cells += Values.RATIO.value

    @classmethod
    def create_id(cls) -> int:
        """- создать идентификационный номер ячейки"""
        cls.count_id += Values.RATIO.value
        return cls.count_id

    def __repr__(self):
        """- вывод матрицы с данными
        для отображении шпаргалки в консоли"""
        if self.is_mine:
            return "M"
        if self.is_open:
            return " "

        return f"{self.count_mine_near}"


class Field(object):
    """- поле"""

    def __init__(self):
        self.cells: List[List[Cell]] = []
        self.count_mine_field: int = Values.EMPTY.value  # уровень сложности, по умолчанью ноль
        self.non_mined_cells: int = Values.EMPTY.value  # количество не заминированных ячеек, по умолчанию ноль

    def get_cell(self, rw: int, cl: int) -> Union[Cell, None]:
        """- получить значение ячейки по номеру столбца и строки"""
        first: int = Values.FIRST_INDEX.value
        second: int = Values.SECOND_INDEX.value
        # проверка входных данных, на границы размера матрицы
        if cl < first or cl > second or rw < first or rw > second:
            return None
        return self.cells[rw][cl]

    def set_difficulty(self, st: str):
        """- установить значение уровня сложности"""
        for cx in Complex:
            if st == cx.name:
                self.count_mine_field = cx.value
                break

    def get_non_mined_cells(self):
        """- получить количество не заминированных ячеек"""
        self.non_mined_cells = Values.FULL_CELLS - self.count_mine_field

    def create_matrix(self, cl: Type[Cell]):
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
        lst: List[int] = [cl.id for cel in self.cells for cl in cel]
        # перемешать список с id рандомно
        random.shuffle(lst)
        # сделать срез по количеству мин, указанные клиентом
        lt: List[int] = lst[: self.count_mine_field]
        # перезаписать матрицу, расставить мины,
        # используя перемешанный рандомно список и обрезанный по указателю сложности,
        # полученному от пользователя
        for cel in self.cells:
            for cl in cel:
                if cl.id in lt:
                    cl.set_mine()

    def open_empty_cells_nearby(self, obj: Cell):
        """- открыть пустые ячейки поблизости"""

        grid: list = Values.grid()
        queue: List[Cell] = [obj]  # очередь

        while queue:

            # берем последнее значение из очереди
            cell: Cell = queue.pop()

            # если у ячейки статус, is_open = True, то такую ячейку пропускаем
            if cell.is_open:
                continue

            # обходим соседние ячейки, используя значения из списка [-1, 0, 1]
            for row_dx in grid:
                for col_dx in grid:

                    # получить переменные для проверки границ матрицы
                    rw: int = operator.add(cell.row, row_dx)
                    cl: int = operator.add(cell.column, col_dx)

                    # проверяем границы матрицы, если значения не существует то пропускаем
                    response: Cell = self.get_cell(rw=rw, cl=cl)

                    if not response:
                        continue

                    # если у ячейки, из ответа, (вдруг) статус мины, то делаем пропуск
                    if response.is_mine:
                        continue

                    # если в свойстве ответа количество мин не равен нолю (пустоте),
                    # и у ячейки статус не открыта, то добавляем ее в очередь
                    if not response.count_mine_near and not response.is_open:
                        queue.append(response)
                    # иначе у ячейки ставим статус открытой is_open = True
                    else:
                        response.set_open()

            # добавляем текущей ячейки (от которой ведется обход) статус открыта is_open = True
            cell.set_open()

    def fill_count_mine_nearby(self):
        """- заполнить матрицу объектов количеством мин по соседству"""

        grid: list = Values.grid()

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
                        rw: int = operator.add(cs.row, row_dx)
                        cl: int = operator.add(cs.column, col_dx)

                        # проверяем границы матрицы, если значения не существует то пропускаем
                        response = self.get_cell(rw=rw, cl=cl)

                        if not response:
                            continue

                        # если проверки проходят, то меняем значение в нашей матрице
                        response.set_count_mine()

    def create_field(self):
        """- создаем поле"""
        # создать матрицу, и заполнить объектами ячейки
        self.create_matrix(cl=Cell)
        # расставить мины
        self.place_mines()
        # делаем подсказки, указываем на количество мин по соседству
        self.fill_count_mine_nearby()
        # получить количество не заминированных ячеек
        self.get_non_mined_cells()

    def init_field(self, level: str):
        """- инициализируем поле, загружаем поле"""
        # получаем уровень сложности, выбранный пользователем
        # и устанавливаем какое будет количество мин на поле
        self.set_difficulty(st=level)
        # создаем поле
        self.create_field()


class Game(object):
    """- уровень игры, варианты окончание игры, победа, поражение, начало игры, конец игры"""

    def __init__(self):
        self.field: Field = Field()
        self.is_flag: bool = False

    def init_game(self):
        """- инициализация игры"""
        # получить данные из формы от GET запроса,
        # с данными уровня сложности
        lst: List[str] = list(request.args.values())

        # инициализируем поле, игры
        self.field.init_field(*lst)
        # обнулить счетчик открытых ячеек
        self.reset_properties()

    def handler(self) -> Union[dict, None]:
        """- обработчик полученной ячейки, проверка на поражения и на победу, на пустоту"""
        # получить значение из формы (POST запрос)
        args: List[Tuple[str, str]] = list(request.form.items())

        # конвертировать значения из строк в целочисленные значения
        coord: Tuple[int, int] = self.convert_to_integer(*args)
        # получить объект выбранной ячейки, из поля
        cell: Cell = self.field.get_cell(*coord)

        # проверка на пустую ячейку,
        # или ячейку с количеством мин
        if cell.is_count_mine() is True:
            # если не пустая, а имеет значение мин рядом,
            # то переводим в открытое состояние
            cell.set_open()
        else:
            # если ячейка пустая, то открыть все рядом пустые ячейки
            self.field.open_empty_cells_nearby(obj=cell)

        # проверка поражения в игре
        if cell.is_mine is True:
            # проверка на поражение в игре, если пользователь столкнулся с миной
            # если поражение передаем словарь с сообщение о проигрыше и имя стиля класса, для подсветки
            self.is_flag = True
            return dict(message="ВЫ ПРОИГРАЛИ", category='error')

        if Cell.count_open_cells >= self.field.non_mined_cells:
            # если победа передаем словарь с сообщение о победе и имя стиля класса, для подсветки
            self.is_flag = True
            return dict(message="ВЫ ВЫГРАЛИ, УРА!!!", category='success')

        return None

    def reset_properties(self):
        """- вернуть свойства в первоначальное состояние"""
        # обнулить счетчик
        Cell.count_open_cells = Values.EMPTY.value
        # установить флаг в первоначальное состояние
        self.is_flag = False

    def restart(self):
        """- перегрузить игру, с выбранным набором сложности, level"""
        self.reset_properties()
        # вернуть свойства в первоначальное состояние
        self.field.create_field()

    @staticmethod
    def convert_to_integer(tup: tuple) -> Tuple[int, int]:
        """- конвертировать полученные данные от кнопки в число"""
        row, column = tup
        return int(row), int(column)
