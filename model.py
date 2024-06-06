import logging
import random
from collections.abc import Callable

class ModelException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class InvalidMoveException(ModelException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class GameOverException(ModelException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class FigureRotation(object):
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
    def __init__(self, projections: list[FigureRotation], current_projection: int) -> None:
        super().__init__()
        assert 0 <= len(projections) <= 4 
        assert 0 <= current_projection < len(projections)
        self.__projections = projections
        self.__current_projection = current_projection

    def get_projection_count(self) -> None:
        return len(self.__projections)
    
    def get_current_projection(self) -> FigureRotation:
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
            FigureRotation([
                [True, True],
                [True, False]]),
                FigureRotation([
                [True, True],
                [False, True]]),
                FigureRotation([
                [False, True],
                [True, True]]),
                FigureRotation([
                [True, False],
                [True, True]])
        ], 0),
        Figure([
            FigureRotation([
                [True, True, False],
                [False, True, True]]),
            FigureRotation([
                [False, True],
                [True, True],
                [True, False]])
        ], 0),
        Figure([
            FigureRotation([
                [False, True, True],
                [True, True, False]]),
            FigureRotation([
                [True, False],
                [True, True],
                [False, True]])
        ], 0),
        Figure([
            FigureRotation([
                [True, True, True, True]]),
            FigureRotation([
                [False, True],
                [False, True],
                [False, True],
                [False, True]])
        ], 0),
        Figure([
            FigureRotation([
                [True, True],
                [True, True]])
        ], 0),
        Figure([
            FigureRotation([
                [False, True, False],
                [True, True, True]]),
            FigureRotation([
                [True, False],
                [True, True],
                [True, False]]),
            FigureRotation([
                [True, True, True],
                [False, True, False]]),
            FigureRotation([
                [False, False, True],
                [False, True, True],
                [False, False, True]])
        ], 0),
        Figure([
            FigureRotation([
                [True, True, True],
                [True, False, False]]),
            FigureRotation([
                [False, True, True],
                [False, False, True],
                [False, False, True]]),
            FigureRotation([
                [False, False, True],
                [True, True, True]]),
            FigureRotation([
                [True, False, False],
                [True, False, False],
                [True, True, False]])
        ], 0),
        Figure([
            FigureRotation([
                [True, True, True],
                [False, False, True],
                ]),
            FigureRotation([
                [False, False, True],
                [False, False, True],
                [False, True, True]]),
            FigureRotation([
                [True, False, False],
                [True, True, True]]),
            FigureRotation([
                [True, True, False],
                [True, False, False],
                [True, False, False]])
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
    
    def set_row(self, row: int) -> None:
        self.__row = row
    
    def get_style_idx(self) -> int:
        return self.__style_idx
    
    def __repr__(self) -> str:
        return f'Cell({self.__row}, {self.__col}, {self.__style_idx})'
    
    def __eq__(self, value: object) -> bool:
        if isinstance(value, Cell):
            c: Cell = value
            return self.__col == c.get_col() and self.__row == c.get_row() and self.__style_idx == c.get_style_idx()
        else:
            raise ValueError(f'Cell object can be compared only to the same type object.')

class Board(object):
    def __init__(self, rows: int, cols: int, cells = []) -> None:
        super().__init__()
        self.__rows = rows
        self.__cols = cols
        self.__cells: list[Cell] = cells

    def get_rows(self):
        return self.__rows

    def get_cols(self):
        return self.__cols

    def get_cells(self) -> list[Cell]:
        return self.__cells
    
    def get_layout(self) -> list[list[bool]]:
        result = [[False] * self.__cols for _ in range(self.__rows)]
        for cell in self.__cells:
            result[cell.get_row()][cell.get_col()] = True
        return result
    
    def is_cell_occupied(self, row, col) -> bool:
        # TODO: Optimize - some sort of topology-based index is needed
        return next((c for c in self.__cells if c.get_row() == row and c.get_col() == col), None) is not None
    
    def check_fit(self, figure: Figure, row: int, col: int) -> bool:
        rel_coords = figure.get_current_projection().get_cells_coords()
        abs_coords = [(r + row, c + col) for (r, c) in rel_coords]
        if not all([0 <= r < self.__rows and 0 <= c < self.__cols for (r, c) in abs_coords]):
            return False
        target_cells_empty = [not self.is_cell_occupied(r, c) for (r, c) in abs_coords]
        return all(target_cells_empty)

    def figure_final_placement(self, cells: list[Cell]) -> None:
        self.__cells.extend(cells)
        logging.debug(f'New board state {self.__cells}')

    def get_completed_rows(self) -> list[int]:
        layout = self.get_layout()
        return [row for row in range(len(layout)) if all(layout[row])]
    
    def remove_rows(self, rows: list[int]) -> None:
        self.__cells = [cell for cell in self.__cells if cell.get_row() not in rows]
        for cell in self.__cells:
            cell.set_row(cell.get_row() + len([r for r in rows if cell.get_row() < r]))

    def reset(self):
        self.__cells = []

class FigureRendering(object):
    def __init__(self, board: Board, figure: Figure, style_idx: int) -> None:
        super().__init__()
        self.__board = board
        self.__figure = figure
        self.__col = int((board.get_cols() - len(figure.get_current_projection().get_layout()[0])) / 2)    # where a figure appears
        self.__row = 0
        self.__style_idx = style_idx
        if not self.__board.check_fit(self.__figure, self.__row, self.__col):
            raise GameOverException(f'Impossible to put new figure on the board.')

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

# TODO: add game level, auto-increment it after every 10 (or ?) lines.
class Game(object):
    def __init__(self, rows: int, cols: int,
                 score_update_callback: Callable[[int], None] = None, 
                 lines_update_callback: Callable[[int], None] = None) -> None:
        super().__init__()
        self.__score = 0
        self.__lines = 0
        self.__board = Board(rows, cols)
        self.__score_update_callback = score_update_callback
        self.__lines_update_callback = lines_update_callback

    def __set_score(self, score: int) -> None:
        self.__score = score
        if self.__score_update_callback:
            self.__score_update_callback(score)

    def __set_lines(self, lines: int) -> None:
        self.__lines = lines
        if self.__lines_update_callback:
            self.__lines_update_callback(lines)

    def get_board(self) -> Board:
        return self.__board

    def get_score(self) -> int:
        return self.__score
    
    def get_lines(self) -> int:
        return self.__lines

    def score_completed_rows(self, number_of_rows: int) -> None:
        self.__set_score(self.__score + number_of_rows * 100)
        self.__set_lines(self.__lines + number_of_rows)

    def score_move_down(self) -> None:
        self.__set_score(self.__score + 1)

    def reset(self) -> None:
      self.__set_score(0)
      self.__set_lines(0)
      self.__board.reset()

if __name__ == '__main__':
    import copy

    # TODO: move tests in a proper place
    cells = [Cell(0, 0, 0),
             Cell(1, 0, 0), Cell(1, 1, 0), Cell(1, 2, 0),
             Cell(2, 0, 0), Cell(2, 1, 0), Cell(2, 2, 0),
             Cell(3, 0, 0), Cell(3, 1, 0), Cell(3, 2, 0)]
    board = Board(4, 3, copy.deepcopy(cells))
    assert board.get_layout() == [[True, False, False], 
                                  [True, True, True], 
                                  [True, True, True], 
                                  [True, True, True]]
    assert board.get_completed_rows() == [1, 2, 3]

    board.remove_rows([1, 2, 3])
    assert board.get_layout() == [[False, False, False],
                                  [False, False, False],
                                  [False, False, False], 
                                  [True, False, False]]
    
    board = Board(4, 3, copy.deepcopy(cells))
    board.remove_rows([1])
    assert board.get_layout() == [[False, False, False],
                                  [True, False, False],
                                  [True, True, True], 
                                  [True, True, True]]
    
    board.remove_rows([3])
    assert board.get_layout() == [[False, False, False],
                                  [False, False, False],
                                  [True, False, False],
                                  [True, True, True]]
    
    board.remove_rows([3])
    assert board.get_layout() == [[False, False, False],
                                  [False, False, False],
                                  [False, False, False],
                                  [True, False, False]]
    
    board.remove_rows([3])
    assert board.get_layout() == [[False, False, False],
                                  [False, False, False],
                                  [False, False, False],
                                  [False, False, False]]

    ###

    cells = [Cell(0, 0, 0),
             Cell(1, 0, 0), Cell(1, 1, 0), Cell(1, 2, 0), Cell(1, 3, 0),
             Cell(2, 1, 0), Cell(2, 2, 0),
             Cell(3, 3, 0), Cell(3, 2, 0), Cell(3, 1, 0), Cell(3, 0, 0)]
    board = Board(4, 4, cells)
    assert board.get_layout() == [[True, False, False, False], 
                                  [True, True, True, True], 
                                  [False, True, True, False], 
                                  [True, True, True, True]]
    assert board.get_completed_rows() == [1, 3]

    board.remove_rows([1, 3])
    assert board.get_layout() == [[False, False, False, False],
                                  [False, False, False, False],
                                  [True, False, False, False], 
                                  [False, True, True, False]]
