import logging
import random

class ModelException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class InvalidMoveException(ModelException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class FigureProjection(object):
    def __init__(self, layout: list[list[bool]]) -> None:
        super().__init__() 
        self.__layout = layout
        self.__cell_coords = self.__calc_cells_coords()

    def __calc_cells_coords(self) -> list[tuple[int, int]]:
        res = []
        for i in range(len(self.__layout)):
            for j in range(len(self.__layout[i])):
                if self.__layout[i][j]:
                    res.append((i, j))
        return res

    def get_layout(self) -> list[list[bool]]:
        return self.__layout
    
    def get_cells_coords(self) -> list[tuple[int, int]]:
        return self.__cell_coords
    
class Figure(object):
    def __init__(self, projections: list[FigureProjection], current_projection: int) -> None:
        super().__init__()
        assert 0 <= len(projections) <= 4 
        assert 0 <= current_projection < len(projections)
        self.__projections = projections
        self.__current_projection = current_projection

    def get_projection_count(self) -> None:
        return len(self.__projections)
    
    def get_current_projection(self) -> FigureProjection:
        return self.__projections[self.__current_projection]
    
    def rotate_counterclockwise(self) -> None:
        self.__current_projection -= 1
        if self.__current_projection < 0:
            self.__current_projection = len(self.__projections) - 1
    
    def rotate_clockwise(self) -> None:
        self.__current_projection += 1
        if self.__current_projection >= len(self.__projections):
            self.__current_projection = 0

class FiguresManager(object):
    FIGURES = [
        Figure([
            FigureProjection([
                [True, True],
                [True, False]]),
                FigureProjection([
                [True, True],
                [False, True]]),
                FigureProjection([
                [False, True],
                [True, True]]),
                FigureProjection([
                [True, False],
                [True, True]])
        ], 0),
        Figure([
            FigureProjection([
                [True, True, False],
                [False, True, True]]),
            FigureProjection([
                [False, True],
                [True, True],
                [True, False]])
        ], 0),
        Figure([
            FigureProjection([
                [False, True, True],
                [True, True, False]]),
            FigureProjection([
                [True, False],
                [True, True],
                [False, True]])
        ], 0),
        Figure([
            FigureProjection([
                [True, True, True, True]]),
            FigureProjection([
                [False, True],
                [False, True],
                [False, True],
                [False, True]])
        ], 0),
        Figure([
            FigureProjection([
                [True, True],
                [True, True]])
        ], 0),
        Figure([
            FigureProjection([
                [False, True, False],
                [True, True, True]]),
            FigureProjection([
                [True, False],
                [True, True],
                [True, False]]),
            FigureProjection([
                [True, True, True],
                [False, True, False]]),
            FigureProjection([
                [False, True],
                [True, True],
                [False, True]])
        ], 0),
    ]

    @classmethod
    def get_random(cls) -> Figure:
        figure = random.choice(cls.FIGURES)
        for _ in range(random.randrange(figure.get_projection_count())):
            figure.rotate_clockwise()
        return figure

class Cell(object):
    """Represents a cell on the board. This is a bridge model to straigh the interfacing with the View."""
    def __init__(self, row: int, col: int, style_idx: int) -> None:
        super().__init__()
        self.__col = col
        self.__row = row
        self.__style_idx = style_idx

    def get_col(self) -> int:
        return self.__col
    
    def get_row(self) -> int:
        return self.__row
    
    def get_style_idx(self) -> int:
        return self.__style_idx
    
    def __repr__(self) -> str:
        return f'Cell({self.__row}, {self.__col}, {self.__style_idx})'
    
    def __eq__(self, value: object) -> bool:
        if isinstance(value, Cell):
            c: Cell = value
            #logging.trace(f'Comparing {self} to {c}')
            return self.__col == c.get_col() and self.__row == c.get_row() and self.__style_idx == c.get_style_idx()
        else:
            raise ValueError(f'Cell object can be compared only to the same type object.')

class Board(object):
    COLS = 12
    ROWS = 25

    def __init__(self) -> None:
        super().__init__()
        self.__cells: list[Cell] = []

    def get_cells(self) -> list[Cell]:
        return self.__cells
    
    def is_cell_occupied(self, row, col) -> bool:
        # TODO: Optimize - some sort of topology-based index is needed
        return next((c for c in self.__cells if c.get_row() == row and c.get_col() == col), None) is not None
    
    def check_fit(self, figure: Figure, row: int, col: int) -> bool:
        rel_coords = figure.get_current_projection().get_cells_coords()
        abs_coords = [(r + row, c + col) for (r, c) in rel_coords]
        if not all([0 <= r < self.ROWS and 0 <= c < self.COLS for (r, c) in abs_coords]):
            return False
        target_cells_empty = [not self.is_cell_occupied(r, c) for (r, c) in abs_coords]
        return all(target_cells_empty)

    def figure_final_placement(self, cells: list[Cell]) -> None:
        self.__cells.extend(cells)
        logging.debug(f'New board state {self.__cells}')

class FigureRendering(object):
    def __init__(self, board: Board, figure: Figure, style_idx: int) -> None:
        super().__init__()
        self.__board = board
        self.__figure = figure
        self.__col = int((Board.COLS - len(figure.get_current_projection().get_layout()[0])) / 2)    # where a figure appears
        self.__row = 0
        self.__style_idx = style_idx

    def get_col(self) -> int:
        return self.__col
    
    def get_row(self) -> int:
        return self.__row
    
    def move_left(self) -> None:
        if self.__board.check_fit(self.__figure, self.__row, self.__col - 1):
            self.__col -= 1
        else:
            raise InvalidMoveException(f'Figure does not fit if moved left.')

    def move_right(self) -> None:
        if self.__board.check_fit(self.__figure, self.__row, self.__col + 1):
            self.__col += 1
        else:
            raise InvalidMoveException(f'Figure does not fit if moved right.')

    def move_down(self) -> None:
        if self.__board.check_fit(self.__figure, self.__row + 1, self.__col):
            self.__row += 1
        else:
            raise InvalidMoveException(f'Figure does not fit if moved down.')

    def rotate_clockwise(self) -> None:
        logging.debug(self.__figure)
        self.__figure.rotate_clockwise()
        if not self.__board.check_fit(self.__figure, self.__row, self.__col):
            self.__figure.rotate_counterclockwise()
            raise InvalidMoveException(f'Figure does not fit if roteated clockwise.')

    def rotate_counterclockwise(self) -> None:
        logging.debug(self.__figure)
        self.__figure.rotate_counterclockwise()
        if not self.__board.check_fit(self.__figure, self.__row, self.__col):
            self.__figure.rotate_clockwise()
            raise InvalidMoveException(f'Figure does not fit if roteated counterclockwise.')

    def to_cells(self) -> list[Cell]:
        cell_coords = self.__figure.get_current_projection().get_cells_coords()
        return [Cell(self.__row + r, self.__col + c, self.__style_idx) for (r, c) in cell_coords]
