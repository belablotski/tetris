import random

class FigureProjection(object):
    def __init__(self, layout: list[list[bool]]) -> None:
        super().__init__() 
        self.__layout = layout

    def get_layout(self):
        return self.__layout

class Figure(object):
    def __init__(self, projections: list[FigureProjection], current_projection: int) -> None:
        super().__init__()
        assert 0 <= len(projections) <= 4 
        assert 0 <= current_projection < len(projections)
        self.__projections = projections
        self.__current_projection = current_projection

    def get_projection_count(self) -> None:
        return len(self.__projections)
    
    def rotate_left(self) -> None:
        self.__current_projection -= 1
        if self.__current_projection < 0:
            self.__current_projection = len(self.__projections) - 1
    
    def rotate_right(self) -> None:
        self.__current_projection += 1
        if self.__current_projection >= len(self.__projections):
            self.__current_projection = 0

class FiguresManager(object):
    def __init__(self) -> None:
        super().__init__()
        self.__figures = [
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
            ], 0)
        ]

    def get_random(self) -> Figure:
        fig = random.choice(self.__figures)
        for i in range(random.randrange(fig.get_projection_count())):
            fig.rotate_right()

class Board(object):
    def __init__(self, cols: int, rows: int) -> None:
        super().__init__()
        self.__cols = cols
        self.__rows = rows
