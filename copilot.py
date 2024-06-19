import logging

from controller import Controller

class Copilot(object):
    def __init__(self, ctr: Controller) -> None:
        super().__init__()
        self.__ctr = ctr

    def build_flight(self):
        logging.info('Build flight')

    def execute_flight(self):
        logging.info('Execute flight')