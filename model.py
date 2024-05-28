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

    def get_layout(self) -> list[list[bool]]:
        return self.__layout
    
    def get_cells_coords(self) -> list[tuple[int, int]]:
        res = []
        for i in range(len(self.__layout)):
            for j in range(len(self.__layout[i])):
                if self.__layout[i][j]:
                    res.append((i, j))
        return res

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
    figures = [
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
        ], 0)
    ]

    @classmethod
    def get_random(cls) -> Figure:
        fig = random.choice(cls.figures)
        for i in range(random.randrange(fig.get_projection_count())):
            fig.rotate_clockwise()
        return fig

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

class RenderingBase(object):
    def __init__(self) -> None:
        super().__init__()

    def to_cells(self) -> list[Cell]:
        pass

class FigureRendering(RenderingBase):
    def __init__(self, figure: Figure, style_idx: int) -> None:
        super().__init__()
        self.__figure = figure
        self.__col = 5
        self.__row = 0
        self.__style_idx = style_idx

    def get_col(self) -> int:
        return self.__col
    
    def get_row(self) -> int:
        return self.__row
    
    def move_left(self) -> None:
        if self.__col > 0:
            self.__col -= 1
        else:
            raise InvalidMoveException(f'Column can not be less than 0.')

    def move_right(self) -> None:
        if self.__col < 10:
            self.__col += 1
        else:
            raise InvalidMoveException(f'Column can not be more than 10 or equal.')

    def move_down(self) -> None:
        if self.__row < 20:
            self.__row += 1
        else:
            raise InvalidMoveException(f'Row can not be more than 20.')

    def rotate_clockwise(self) -> None:
        logging.debug(self.__figure)
        self.__figure.rotate_clockwise()

    def rotate_counterclockwise(self) -> None:
        logging.debug(self.__figure)
        self.__figure.rotate_counterclockwise()

    def to_cells(self) -> list[Cell]:
        cell_coords = self.__figure.get_current_projection().get_cells_coords()
        return [Cell(self.__row + r, self.__col + c, self.__style_idx) for (r, c) in cell_coords]

class Board(object):
    def __init__(self, cols: int, rows: int) -> None:
        super().__init__()
        self.__cols = cols
        self.__rows = rows
