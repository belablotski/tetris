import logging

from controller import Controller

class Copilot(object):
    def __init__(self, ctr: Controller) -> None:
        super().__init__()
        self.__flight_execution_interval_ms = 300
        self.__ctr = ctr

    def get_flight_execution_interval_ms(self) -> int:
        return self.__flight_execution_interval_ms

    def build_flight(self) -> None:
        logging.info('Build flight')

    def execute_flight(self) -> None:
        logging.info('Execute flight')