import logging

class Controller(object):
    def __init__(self) -> None:
        super().__init__()
        pass

    def move_left(self) -> None:
        logging.debug('Move left')

    def move_right(self) -> None:
        logging.debug('Move right')

    def rotate_clockwise(self) -> None:
        logging.debug('Rotate clockwise')

    def rotate_counterclockwise(self) -> None:
        logging.debug('Rotate counterclockwise')

    def drop(self) -> None:
        logging.debug('Drop')