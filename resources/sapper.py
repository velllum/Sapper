import operator
import random

from enum import Enum
from typing import List, Tuple, Optional

from flask import request

import resources.iterator as it


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
    def graph() -> List[int]:
        """- список с значениями для обхода ячеек
        по вертикали, горизонтали и диагонали"""
        return [-1, 0, 1]

    @staticmethod
    def coord_crawl_cells() -> List[Tuple[int, int]]:
        """- получить список с координатами ячеек обхода,
        для иенения свойств"""
        return [
            (row, col)
            for row in Values.graph()
            for col in Values.graph()
        ]


class Cell:
    """- ячейки"""

    def __init__(self, row, column, cl_id):
        self.is_mine: bool = False  # ячейка мина или нет
        self.is_open: bool = False  # ячейка скрыто или нет
        self.row: int = row  # номер строки
        self.column: int = column  # номер колонки
        self.id: int = cl_id  # порядковый номер
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
        self.is_open = True

    def is_count_mine(self):
        """- проверка если значение больше ноля, то True"""
        if self.count_mine_near != Values.EMPTY.value:
            return True
        return False

    def __repr__(self):
        """- вывод матрицы с данными
        для отображении шпаргалки в консоли"""
        if self.is_mine:
            return "M"
        if self.is_open:
            return " "

        return f"{self.count_mine_near}"


class Field:
    """- поле"""

    def __init__(self):
        self.cells: List[List[Cell]] = []  # матрица с ячейками
        self.count_mine_field: int = Values.EMPTY.value  # уровень сложности, по умолчанью ноль
        self.non_mined_cells: int = Values.EMPTY.value  # количество не заминированных ячеек, по умолчанию ноль
        self.count_id: int = Values.EMPTY.value  # счетчик созданных id ячеек
        self.count_open_cells: int = Values.EMPTY.value  # счетчик количества открытых ячеек на поле
        self.is_disabled: bool = False  # состояние поля, для показа в шаблоне представления (показать или скрыть)
        self.coord_cells: List[Tuple[int, int]] = self.shape_coord_cells_matrix()

    def get_cell(self, rw: int, cl: int) -> Optional[Cell]:
        """- получить значение ячейки по номеру столбца и строки"""
        first: int = Values.FIRST_INDEX.value
        second: int = Values.SECOND_INDEX.value
        # проверка входных данных, на границы размера матрицы
        if cl < first or cl > second or rw < first or rw > second:
            return None
        return self.cells[rw][cl]

    def set_count_mine_field(self, st: str):
        """- установить количество мин, по выбранному уровню сложности"""
        for cx in Complex:
            if st == cx.name:
                self.count_mine_field = cx.value
                break

    def set_open_cell(self, cl: Cell):
        """- поменять значения с закрытой на открытое"""
        # проверка открыта ли ячейка поля
        if not cl.is_open:
            # подсчет количества открытых ячеек
            self.set_count_open_cells()
        cl.set_open()

    def set_count_open_cells(self):
        """- увеличить количество ячеек, которые были открыты"""
        self.count_open_cells += Values.RATIO.value
        return self.count_open_cells

    def reset_count_open_cells(self):
        """- сбросить счетчик количества открытых ячеек на поле"""
        self.count_open_cells = Values.EMPTY.value

    def get_non_mined_cells(self):
        """- получить количество не заминированных ячеек"""
        self.non_mined_cells = Values.FULL_CELLS - self.count_mine_field

    @staticmethod
    def shape_coord_cells_matrix():
        """- сформировать список координат ячеек матрицы"""
        coordinates: List[Tuple[int, int]] = [
            (row, col)
            for col in list(range(Values.VERTICAL.value))
            for row in list(range(Values.HORIZON.value))
        ]
        return coordinates

    def create_matrix(self):
        """- создать матрицу 15X15"""
        lst = [
            [
                # добавляем объект ячейки в матрицу
                Cell(row=row, column=col, cl_id=self.create_id())
                for col in range(Values.VERTICAL.value)
            ]
            for row in range(Values.HORIZON.value)
        ]

        self.cells = lst

    def create_id(self) -> int:
        """- создать идентификационный номер ячейки"""
        self.count_id += Values.RATIO.value
        return self.count_id

    def reset_count_id(self):
        """- сбросить счетчик, созданных id номеров"""
        self.count_id = Values.EMPTY.value

    def place_mines(self):
        """- расставить мины"""
        # перемешать список с id рандомно
        random.shuffle(self.coord_cells)
        # сделать срез по количеству мин, указанные клиентом
        coord_mines: List[Tuple[int, int]] = self.coord_cells[: self.count_mine_field]
        # перезаписать матрицу, расставить мины
        for coord in coord_mines:
            cell = self.get_cell(*coord)
            cell.set_mine()

    def iterate_cells(self, row: int, col: int) -> List[Cell]:
        """- получить ячейки через итерируемы объект"""
        return it.Iterator.iterate_object(field=self, cell=self.get_cell(rw=row, cl=col))

    def open_empty_cells_nearby(self, obj: Cell):
        """- открыть пустые ячейки поблизости"""

        queue: List[Cell] = [obj]  # очередь

        while queue:

            # берем последнее значение из очереди
            cell: Cell = queue.pop()

            # если у ячейки статус, is_open = True, то такую ячейку пропускаем
            if cell.is_open:
                continue

            # # перебрать все ячейки, относительно текущей ячейки
            for coord in Values.coord_crawl_cells():
                # если у ячейки, из ответа, (вдруг) статус мины, то делаем пропуск

                row, column = coord

                coord_rw: int = operator.add(cell.row, row)
                coord_cl: int = operator.add(cell.column, column)

                cl = self.get_cell(rw=coord_rw, cl=coord_cl)

                if not cl:
                    continue

                if cl.is_mine:
                    continue

                # если в свойстве ответа количество мин не равен нолю (пустоте),
                # и у ячейки статус не открыта, то добавляем ее в очередь
                if not cl.count_mine_near and not cl.is_open:
                    queue.append(cl)
                # иначе у ячейки ставим статус открытой is_open = True
                else:
                    self.set_open_cell(cl)

            # добавляем текущей ячейки (от которой ведется обход) статус открыта is_open = True
            self.set_open_cell(cell)

    def fill_count_mine_nearby(self):
        """- заполнить матрицу объектов количеством мин по соседству"""

        # перебрать список сформированых координат ячеек и применить их к матрице
        for current_coord in self.coord_cells:
            # найти мину, для добавления значений соседним ячейкам
            cell = self.get_cell(*current_coord)

            if not cell.is_mine:
                continue

            for coord in Values.coord_crawl_cells():

                row, column = coord

                coord_rw: int = operator.add(cell.row, row)
                coord_cl: int = operator.add(cell.column, column)

                cl = self.get_cell(rw=coord_rw, cl=coord_cl)

                if not cl:
                    continue

                cl.set_count_mine()

    def reset_properties(self):
        """- вернуть свойства в первоначальное состояние"""
        # обнулить счетчики для подсчета открытых ячеек, создания id
        self.reset_count_open_cells()
        self.reset_count_id()
        # установить флаг в первоначальное состояние
        self.is_disabled = False

    def create_field(self):
        """- создаем поле"""
        # создать матрицу, и заполнить объектами ячейки
        self.create_matrix()
        # расставить мины
        self.place_mines()
        # делаем подсказки, указываем на количество мин по соседству
        self.fill_count_mine_nearby()
        # получить количество не заминированных ячеек
        self.get_non_mined_cells()
        # обнулить счетчики и значение свойст к первоначальному состоянию, после предедущей игры
        self.reset_properties()

    def init_field(self, level: str):
        """- инициализируем поле, загружаем поле"""
        # получаем уровень сложности, выбранный пользователем
        # и устанавливаем какое будет количество мин на поле
        self.set_count_mine_field(level)
        # создаем поле
        self.create_field()


class Game:
    """- уровень игры, варианты окончание игры, победа, поражение, начало игры, конец игры"""

    def __init__(self):
        self.field: Field = Field()

    def init_game(self):
        """- инициализация игры"""
        # получить данные из формы от GET запроса,
        # с данными уровня сложности
        lst: List[str] = list(request.args.values())
        # инициализируем поле, игры
        self.field.init_field(*lst)

    def restart(self):
        """- перегрузить игру, с выбранным набором сложности, level"""
        self.field.create_field()

    @staticmethod
    def convert_to_integer(tup: tuple) -> Tuple[int, int]:
        """- конвертировать полученные данные от кнопки в число"""
        row, column = tup
        return int(row), int(column)

    def handler(self) -> Optional[dict]:
        """- обработчик полученной ячейки, проверка на поражения и на победу, на пустоту"""
        # получить значение из формы (POST запрос)
        args: List[Tuple[str, str]] = list(request.form.items())

        # конвертировать значения из строк в целочисленные значения
        coord: Tuple[int, int] = self.convert_to_integer(*args)
        # получить объект выбранной ячейки, из поля
        cell: Cell = self.field.get_cell(*coord)

        # проверка на пустую ячейку,
        # или ячейку с количеством мин
        if cell.is_count_mine():
            # если не пустая, а имеет значение мин рядом,
            # то переводим в открытое состояние
            self.field.set_open_cell(cell)
        else:
            # если ячейка пустая, то открыть все рядом пустые ячейки
            self.field.open_empty_cells_nearby(cell)

        # проверка поражения в игре
        if cell.is_mine:
            # проверка на поражение в игре, если пользователь столкнулся с миной
            # если поражение передаем словарь с сообщение о проигрыше и имя стиля класса, для подсветки
            self.field.is_disabled = True
            return dict(message="ВЫ ПРОИГРАЛИ", category='error')

        if self.field.count_open_cells >= self.field.non_mined_cells:
            # если победа передаем словарь с сообщение о победе и имя стиля класса, для подсветки
            self.field.is_disabled = True
            return dict(message="ВЫ ВЫГРАЛИ, УРА!!!", category='success')

        return None
