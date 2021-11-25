import operator
from typing import Optional, Generator, Iterator

import resources.sapper as sp


class IteratorCells:
    """- базовый класс итератора"""

    def __init__(self, cell, field, coord_row, coord_col):
        self.cell: sp.Cell = cell  # объект ячейки
        self.field: sp.Field = field  # объект поля
        self.coord_row: int = coord_row
        self.coord_col: int = coord_col
        self.count: int = sp.Values.EMPTY.value  # счетчик итераций

    def __iter__(self):
        """- переопределяем метод получения объекта итерации"""
        return self

    def __next__(self) -> Optional[sp.Cell]:
        """- переопределяем метод текущей итерации"""

        # получаем ячейку из матрицы, по координатам
        return self.field.get_cell(
            rw=operator.add(self.cell.row, self.coord_row),
            cl=operator.add(self.cell.column, self.coord_col),
        )


class GeneratorCells:
    """- получаем данные от клиента"""

    coord = sp.Values.coord_crawl_cells()
    count = sp.Values.EMPTY

    @classmethod
    def object(cls, field: sp.Field, cell: sp.Cell) -> Iterator[sp.Cell]:

        while True:

            # проверка итерации, если больше длины
            # то вызываем сановку
            if cls.count >= len(cls.coord):
                # сбрасываем счетчик
                cls.count = sp.Values.EMPTY
                break

            # получить значение для изменения координат
            row, col = cls.coord[cls.count]

            # получить ячейки
            cl = IteratorCells(
                cell=cell,
                field=field,
                coord_row=row,
                coord_col=col,
            )

            # увеличиваем счетчик
            cls.count += sp.Values.RATIO

            yield next(cl)
