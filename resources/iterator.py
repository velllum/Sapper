import operator
from typing import List

import resources as sp


class BaseIterator:
    """- базовый класс итератора"""

    def __init__(self, cell, field):
        self.cell: sp.Cell = cell  # объект ячейки
        self.field: sp.Field = field  # объект поля
        self.graph: List[int] = sp.Values.graph()  # берем список с заготовленными значениями для обхода
        self.count: int = sp.Values.EMPTY.value  # счетчик итераций

    def __iter__(self):
        """- переопределяем метод получения объекта итерации"""
        return self

    def __next__(self):
        """- переопределяем метод текущей итерации"""

        # проверяем конец последовательности
        if len(self) < self.count:
            raise StopIteration

        # берем значение из списка [-1, 0, 1]
        coord = self.graph[self.count]

        # увеличиваем счетчик
        self.count += 1

        return coord

    def __len__(self):
        """- переопределяем метод подсчета длинны последовательности """
        return len(self.graph) - sp.Values.RATIO.value

    @staticmethod
    def get_coord(coord_a: int = 0, coord_b: int = 0) -> int:
        """- получить кордиту, добавив указатель из списка [-1, 0, 1], относительно находящейся ячейки"""
        return operator.add(coord_a, coord_b)


class ColumnIterator(BaseIterator):
    """- итератор обхода по колонкам"""

    def __init__(self, coord_row, cell, field):
        super().__init__(cell, field)
        self.coord_row: int = coord_row

    def __next__(self):
        coord_col = super().__next__()

        # получаем ячейку из матрицы, по координатам
        cell = self.field.get_cell(
            rw=self.get_coord(coord_a=self.cell.row, coord_b=self.coord_row),
            cl=self.get_coord(coord_a=self.cell.column, coord_b=coord_col),
        )

        return cell


class RowIterator(BaseIterator):
    """- итератор обхода по строкам"""

    def __init__(self, field, cell):
        super().__init__(cell, field)
        self.cell: sp.Cell = cell

    def __next__(self) -> ColumnIterator:
        coord_row = super().__next__()

        iterator = ColumnIterator(
            coord_row=coord_row,
            cell=self.cell,
            field=self.field
        )

        return iterator


class Iterator:
    """- получаем данные от клиента"""

    @classmethod
    def iterate_object(cls, field, cell) -> List:
        """- перебрать итерируемый объект и добавить его в список если он не None"""

        # собрать объекты всех ячеек что рядом в общий список
        cells = [
            cl
            # создаем объект итератора по ячейкам, относительно текущей ячейки
            for itr in RowIterator(field, cell)
            # перебираем вложенный итератор
            for cl in itr
            # делаем проверку на пустоту
            if cl
        ]

        return cells




