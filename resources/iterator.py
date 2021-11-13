import operator
from typing import List, Optional

import resources as sp


class BaseIterator:
    """- базовый класс итератора"""

    def __init__(self, cell, field):
        self.cell: sp.Cell = cell
        self.field: sp.Field = field
        self.graph: List[int] = sp.Values.graph()
        self.count: int = sp.Values.EMPTY.value

    def __iter__(self):
        return self

    def __next__(self):
        if len(self) < self.count:
            raise StopIteration

        coord = self.graph[self.count]
        self.count += 1

        return coord

    def __len__(self):
        return len(self.graph) - sp.Values.RATIO.value

    @staticmethod
    def get_coord(coord_a: int = 0, coord_b: int = 0) -> int:
        """- получить кордиту, добавив указатель из списка [-1, 0, 1], относительно находящейся ячейки"""
        return operator.add(coord_a, coord_b)


class AggregateIterator(BaseIterator):
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


class Iterator(BaseIterator):
    """- итератор обхода по строкам"""

    def __init__(self, field, cell):
        super().__init__(cell, field)
        self.cell: sp.Cell = cell

    def __next__(self) -> AggregateIterator:
        coord_row = super().__next__()

        return AggregateIterator(
            coord_row=coord_row,
            cell=self.cell,
            field=self.field
        )
