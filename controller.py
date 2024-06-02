import logging

from model import Board, FiguresManager, FigureRendering, InvalidMoveException
from view import CellRenderer, CellStyles, BoardRenderer

class Controller(object):
    def __init__(self, board: Board, figure_renderer: CellRenderer, board_renderer: BoardRenderer) -> None:
        super().__init__()
        self.__push_down_interval_ms = 1000
        self.__board = board
        self.__figure_rendering: FigureRendering = None
        self.__figure_renderer = figure_renderer
        self.__board_renderer = board_renderer

    def __refresh_display(self) -> None:
        self.__figure_renderer.display(self.__figure_rendering.to_cells())

    def __next_figure(self) -> None:
        if self.__figure_rendering:
            logging.debug(f'Put figure on the board as cells {self.__figure_rendering.to_cells()}')
            self.__board.figure_final_placement(self.__figure_rendering.to_cells())
            self.__board_renderer.display(self.__board.get_cells())
            self.__figure_renderer.reset()
        figure = FiguresManager.get_random()
        logging.info(f'New figure {figure}: {figure.get_current_projection()}')
        self.__figure_rendering = FigureRendering(self.__board, figure, CellStyles.get_random_style_idx())
        self.__refresh_display()

    def __move(self, mv_func, start_over_if_fails):
        try:
            mv_func()
            self.__refresh_display()
        except InvalidMoveException as e:
            logging.debug(f'Blocking move: {e}')
            if start_over_if_fails:
                self.__next_figure()

    def get_push_down_interval_ms(self) -> int:
        return self.__push_down_interval_ms

    def move_left(self) -> None:
        logging.debug('Move left')
        self.__move(self.__figure_rendering.move_left, False)

    def move_right(self) -> None:
        logging.debug('Move right')
        self.__move(self.__figure_rendering.move_right, False)

    def rotate_clockwise(self) -> None:
        logging.debug('Rotate clockwise')
        self.__move(self.__figure_rendering.rotate_clockwise, False)

    def rotate_counterclockwise(self) -> None:
        logging.debug('Rotate counterclockwise')
        self.__move(self.__figure_rendering.rotate_counterclockwise, False)

    def drop(self) -> None:
        logging.debug('Drop')
        self.__move(self.__figure_rendering.move_down, True)

    def push_down(self) -> None:
        logging.debug('Push-down')
        self.__move(self.__figure_rendering.move_down, True)

    def start_game(self) -> None:
        self.__next_figure()
