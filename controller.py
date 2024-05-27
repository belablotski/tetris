import logging

from model import Figure, FiguresManager, FigureRendering, InvalidMoveException
from view import CellRenderer

class Controller(object):
    def __init__(self, cell_renderer: CellRenderer) -> None:
        super().__init__()
        self.__push_down_interval_ms = 1000
        self.__figure_rendering: FigureRendering = None
        self.__cell_renderer = cell_renderer

    def __refresh_display(self) -> None:
        self.__cell_renderer.display(self.__figure_rendering.to_cells())

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

    def drop(self) -> None:
        logging.debug('Drop')
        self.__figure_rendering.move_down()
        self.__refresh_display()

    def push_down(self) -> None:
        logging.debug('Push-down')
        self.__figure_rendering.move_down()
        self.__refresh_display()

    def next_figure(self) -> None:
        figure = FiguresManager.get_random()
        logging.info(f'New figure {figure}: {figure.get_current_projection()}')
        self.__figure_rendering = FigureRendering(figure)
        self.__refresh_display()