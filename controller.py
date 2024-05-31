import logging

from model import Board, FiguresManager, FigureRendering, InvalidMoveException
from view import CellRenderer, CellStyles, BoardRenderer

class Controller(object):
    def __init__(self, board: Board, cell_renderer: CellRenderer, board_renderer: BoardRenderer) -> None:
        super().__init__()
        self.__push_down_interval_ms = 1000
        self.__board = board
        self.__figure_rendering: FigureRendering = None
        self.__cell_renderer = cell_renderer
        self.__board_renderer = board_renderer

    def __refresh_display(self) -> None:
        self.__cell_renderer.display(self.__figure_rendering.to_cells())

    def __next_figure(self) -> None:
        if self.__figure_rendering:
            logging.debug(f'Put figure on the board as cells {self.__figure_rendering.to_cells()}')
            self.__board.figure_final_placement(self.__figure_rendering.to_cells())
            self.__board_renderer.display(self.__board.get_cells())
            self.__cell_renderer.reset()
        figure = FiguresManager.get_random()
        logging.info(f'New figure {figure}: {figure.get_current_projection()}')
        self.__figure_rendering = FigureRendering(self.__board, figure, CellStyles.get_random_style_idx())
        self.__refresh_display()

    def get_push_down_interval_ms(self) -> int:
        return self.__push_down_interval_ms

    def move_left(self) -> None:
        logging.debug('Move left')
        try:
            self.__figure_rendering.move_left()
            self.__refresh_display()
        except InvalidMoveException as e:
            logging.debug(f'Blocking move left: {e}')

    def move_right(self) -> None:
        logging.debug('Move right')
        try:
            self.__figure_rendering.move_right()
            self.__refresh_display()
        except InvalidMoveException as e:
            logging.debug(f'Blocking move right: {e}')

    def rotate_clockwise(self) -> None:
        logging.debug('Rotate clockwise')
        self.__figure_rendering.rotate_clockwise()
        self.__refresh_display()

    def rotate_counterclockwise(self) -> None:
        logging.debug('Rotate counterclockwise')
        self.__figure_rendering.rotate_counterclockwise()
        self.__refresh_display()

    def __go_down(self):
        try:
            self.__figure_rendering.move_down()
            self.__refresh_display()
        except InvalidMoveException as e:
            logging.debug(f'Blocking move down: {e}')

            self.__next_figure()

    def drop(self) -> None:
        logging.debug('Drop')
        self.__go_down()

    def push_down(self) -> None:
        logging.debug('Push-down')
        self.__go_down()

    def start_game(self) -> None:
        self.__next_figure()
