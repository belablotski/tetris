import logging, random
import tkinter as tk
from model import Cell

class CellStyles(object):
    STYLES = [
        ('yellow', 'green'),
        ('lightgreen', 'blue'),
        ('steelblue', 'violet'),
        ('coral3', 'gold4'),
    ]

    @classmethod
    def get_random_style_idx(cls) -> int:
        return random.randrange(len(cls.STYLES))
    
    @classmethod
    def get_style(cls, style_idx: int) -> tuple[str, str]:
        return cls.STYLES[style_idx]

class CellRenderer(object):
    CELL_SIZE_PX = 30

    def __init__(self, canvas: tk.Canvas) -> None:
        super().__init__()
        self.__canvas = canvas
        self.__prev_cells: list[Cell] = []

    def __get_changed_cells(self, cells: list[Cell]) -> tuple[list[Cell], list[Cell]]:
        cells_to_put = []
        cells_to_remove = []

        def is_cell_in(cell: Cell, cells: list[Cell]) -> bool:
            for c in cells:
                if c == cell:
                    return True
            return False
        
        # TODO: optimize
        for c in cells:
            if not is_cell_in(c, self.__prev_cells):
                cells_to_put.append(c)

        for pc in self.__prev_cells:
            if not is_cell_in(pc, cells):
                cells_to_remove.append(pc)

        return (cells_to_put, cells_to_remove)

    def __calc_cell_polygon(self, cell: Cell) -> list[int]:
        d = self.CELL_SIZE_PX
        m = 3
        x = cell.get_col() * d
        y = cell.get_row() * d
        return [x, y, x+d-m, y, x+d-m, y+d-m, x, y+d-m]
        
    def __render_cell(self, cell: Cell) -> None:
        (fill, outline) = CellStyles.get_style(cell.get_style_idx())
        self.__canvas.create_polygon(self.__calc_cell_polygon(cell), outline=outline, fill=fill, width=3)

    def __erase_cell(self, cell: Cell) -> None:
        bg = self.__canvas['background']
        self.__canvas.create_polygon(self.__calc_cell_polygon(cell), outline=bg, fill=bg, width=3)

    def display(self, cells: list[Cell]) -> None:
        (cells_to_put, cells_to_remove) = self.__get_changed_cells(cells)
        logging.debug(f'Previous cells: {self.__prev_cells}')
        logging.debug(f'Cells to put: {cells_to_put}')
        logging.debug(f'Cells to remove: {cells_to_remove}')

        for cell in cells_to_remove:
            self.__prev_cells.remove(cell)
            self.__erase_cell(cell)

        for cell in cells_to_put:
            self.__prev_cells.append(cell)
            self.__render_cell(cell)
