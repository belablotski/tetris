import logging
from collections.abc import Callable

from model import Game, FiguresManager, FigureRendering, InvalidMoveException, GameOverException
from view import CellStyles, BoardView

class Controller(object):
    def __init__(self, game: Game, board_view: BoardView, game_over_callback: Callable[[], None] = None) -> None:
        super().__init__()
        self.__push_down_interval_ms = 1000
        self.__game = game
        self.__figure_rendering: FigureRendering = None
        self.__board_view = board_view
        self.__game_over_callback = game_over_callback

    def __refresh_display(self) -> None:
        self.__board_view.get_figure_renderer().display(self.__figure_rendering.to_cells())

    def __next_figure(self) -> None:
        if self.__figure_rendering:
            logging.debug(f'Put figure on the board as cells {self.__figure_rendering.to_cells()}')
            self.__game.get_board().figure_final_placement(self.__figure_rendering.to_cells())
            completed_rows = self.__game.get_board().get_completed_rows()
            # TODO: It will be great to remove them one by one with some sort of animation.
            if completed_rows:
                self.__game.score_completed_rows(len(completed_rows))
                self.__game.get_board().remove_rows(completed_rows)
                self.__board_view.get_board_renderer().reset()
                self.__board_view.get_board_renderer().clear_canvas()
            self.__board_view.get_board_renderer().display()
            self.__board_view.get_figure_renderer().reset()
        figure = FiguresManager.get_random()
        logging.info(f'New figure {figure.get_current_projection().get_layout()}')
        try:
            self.__figure_rendering = FigureRendering(self.__game.get_board(), figure, CellStyles.get_random_style_idx())
            self.__refresh_display()
        except GameOverException:
            self.__game_over_callback()

    def __move(self, mv_func, start_over_if_fails):
        try:
            mv_func()
            self.__refresh_display()
        except InvalidMoveException as e:
            logging.debug(f'Blocking move: {e}')
            if start_over_if_fails:
                self.__next_figure()

    def __go_down(self):
        self.__game.score_move_down()
        self.__move(self.__figure_rendering.move_down, True)

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
        self.__go_down()

    def push_down(self) -> None:
        logging.debug('Push-down')
        self.__go_down()

    def start_game(self) -> None:
        self.__next_figure()

    def reset(self) -> None:
        self.__game.reset()
        self.__board_view.reset()
        self.__figure_rendering = None
        self.start_game()
