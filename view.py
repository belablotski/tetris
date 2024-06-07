import logging, random
from tkinter import Canvas
from model import Board, Cell

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
    def __init__(self, canvas: Canvas, cell_size_px: int) -> None:
        super().__init__()
        self.__canvas = canvas
        self.__cell_size_px = cell_size_px
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
        sz = self.__cell_size_px
        margin = 3
        x = cell.get_col() * sz
        y = cell.get_row() * sz
        return [x, y, x+sz-margin, y, x+sz-margin, y+sz-margin, x, y+sz-margin]
        
    def __render_cell(self, cell: Cell) -> None:
        (fill, outline) = CellStyles.get_style(cell.get_style_idx())
        self.__canvas.create_polygon(self.__calc_cell_polygon(cell), outline=outline, fill=fill, width=3)

    def __erase_cell(self, cell: Cell) -> None:
        bg = self.__canvas['background']
        self.__canvas.create_polygon(self.__calc_cell_polygon(cell), outline=bg, fill=bg, width=3)

    def _get_canvas(self):
        return self.__canvas

    def reset(self) -> None:
        self.__prev_cells = []
    
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

class BoardRenderer(CellRenderer):
    def __init__(self, board: Board, canvas: Canvas, cell_size_px: int) -> None:
        super().__init__(canvas, cell_size_px)
        self.__board = board

    def display(self) -> None:
        return super().display(self.__board.get_cells())

    def clear_canvas(self) -> None:
        self._get_canvas().delete("all")

class BoardView(object):
    def __init__(self, board: Board, canvas: Canvas, cell_size_px) -> None:
        super().__init__()
        self.__figure_renderer = CellRenderer(canvas, cell_size_px)
        self.__board_renderer = BoardRenderer(board, canvas, cell_size_px)

    def get_figure_renderer(self) -> CellRenderer:
        return self.__figure_renderer
    
    def get_board_renderer(self) -> BoardRenderer:
        return self.__board_renderer

    def reset(self) -> None:
        self.__board_renderer().reset()
        self.__board_renderer().clear_canvas()
        self.__figure_renderer().reset()
