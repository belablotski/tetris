import google.generativeai as genai
import logging

from model import FigureRendering
from controller import Controller

class Copilot(object):
    def __init__(self, ctr: Controller) -> None:
        super().__init__()
        self.__flight_execution_interval_ms = 300
        self.__ctr = ctr
        self.__model_version = 'models/gemini-1.5-flash-latest'
        self.__instruction = """You are an expert Tetris player. You will be helping another player to win the game of Tetris.

You will be asked for an advice on what to do with the piece in hands. The tetromino you can move is at the top of the game field.

The game board (also known as "well" or "matrix") has 25 rows and 12 columns. Each cell is binary coded, where 0 means an empty 
(vacant) cell and 1 means an occupied cell.

Your response should be a sequence of actions - what to do with the piece to land it at the desired position, where the piece
completes some lines or put (if line completion is not feasible) put the piece strategically to make further line completion
easier. The sequence of actions is the list of allowed actions: "move left", "move right", "rotate clockwise", 
"rotate counterclockwise", "release".

For example:

000011100000
000000100000
000000000000
000000000000
000000000000
000000000000
000000000000
000000000000
000000000000
000000000000
000000000000
000000000000
000000000000
000000000000
000000000000
000000000000
000000000000
000000000000
000000000000
000000000000
000000000000
101111111111
101111111111
111110111111
111110111111

The sequence of actions to land the piece will be "rotate counterclockwise", "move left", "move left", "move left", "release".
The "release" must be the last command since after that the piece just drops down."""
        self.__model = genai.GenerativeModel(self.__model_version, system_instruction=self.__instruction)

    def __ask_ai(self, well_text: str) -> None:
        prompt = """
Advise how to land the tetromino currently located at the top (the first row) on the board of 12 cols and 25 rows,
where 0 represents a free cell and 1 means that the cell is occupied.

""" + well_text 
        
        response = self.__model.generate_content(prompt)

        print('*' * 100)
        print(response.text)


    def get_flight_execution_interval_ms(self) -> int:
        return self.__flight_execution_interval_ms

    def build_flight(self, figure_rendering: FigureRendering, google_ai_api_key: str) -> None:
        logging.info(f'Build flight, calling Google AI with API key {google_ai_api_key[:5]}...')
        assert google_ai_api_key is not None
        well = figure_rendering.get_layout()
        well_text = '\n'.join([''.join(['1' if cell else '0' for cell in row]) for row in well])
        genai.configure(api_key=google_ai_api_key)
        self.__ask_ai(well_text)

    def execute_flight(self) -> None:
        logging.info('Execute flight')
