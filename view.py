import logging
import tkinter as tk
from model import Cell

class CellRenderer(object):
    def __init__(self, canvas: tk.Canvas) -> None:
        super().__init__()
        self.__canvas = canvas
        self.__prev_cells: list[Cell] = []

    def __get_changed_cells(self, cells: list[Cell]) -> tuple[list[Cell], list[Cell]]:
        cells_to_put = []
        cells_to_remove = []
        
        for c in cells:
            c_already_there = False
            for pc in self.__prev_cells:
                if c == pc:
                    c_already_there = True
            if not c_already_there:
                cells_to_put.append(c)

        for pc in self.__prev_cells:
            pc_was_there = False
            for c in cells:
                if c == pc:
                    pc_was_there = True
            if not pc_was_there:
                cells_to_remove.append(c)

        return (cells_to_put, cells_to_remove)

    def display(self, cells: list[Cell]) -> None:
        (cells_to_put, cells_to_remove) = self.__get_changed_cells(cells)
        logging.debug(f'Previous cells: {self.__prev_cells}')
        logging.debug(f'Cells to put: {cells_to_put}')
        logging.debug(f'Cells to remove: {cells_to_remove}')

        for cell in cells_to_remove:
            x = cell.get_col() * 20
            y = cell.get_row() * 20
            points = [x, y, x+20, y, x+20, y+20, x, y+20]
            self.__canvas.create_polygon(points, outline='green', fill='white', width=1)

        for cell in cells_to_put:
            x = cell.get_col() * 20
            y = cell.get_row() * 20
            points = [x, y, x+20, y, x+20, y+20, x, y+20]
            self.__canvas.create_polygon(points, outline='green', fill='yellow', width=3)

        self.__prev_cells = [c for c in self.__prev_cells if len([x for x in cells_to_remove if x == c]) == 0] + cells_to_put
