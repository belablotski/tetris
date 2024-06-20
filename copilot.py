import google.generativeai as genai
import json, logging
from collections.abc import Callable

from model import FigureRendering
from controller import Controller

class Copilot(object):
    def __init__(self, ctr: Controller) -> None:
        super().__init__()
        self.__flight_execution_interval_ms = 300
        self.__ctr = ctr
        self.__flight_ops = []
        self.__current_fligh_op = 0
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
        self.__model = genai.GenerativeModel(self.__model_version,
                                             system_instruction=self.__instruction,
                                             generation_config={"temperature": 0})

    def __ask_ai(self, well_text: str) -> None:
        prompt = f"""Advise how to land the tetromino currently located at the top (the first row) on the board of 12 cols and 25 rows,
where 0 represents a free cell and 1 means that the cell is occupied.

{well_text}

Generate list of entities in text based on the following Python class structure:
list[str]
"""
        
        response = self.__model.generate_content(prompt,
                                                 generation_config={"response_mime_type": "application/json"})
        logging.debug(f'AI response:{response}')
        logging.info(f'AI response text:{response.text}')
        return response.text

    def __parse_ai_response(self, text: str) -> list[Callable[[], None]]:
        result: list[Callable[[], None]] = []
        errors: list[str] = []
        moves = json.loads(text)
        for move in moves:
            logging.info(f'Processing move {move}')
            if 'left' in move:
                result.append(self.__ctr.move_left)
            elif 'right' in move:
                result.append(self.__ctr.move_right)
            elif 'clockwise' in move:
                result.append(self.__ctr.rotate_clockwise)
            elif 'counter' in move:
                result.append(self.__ctr.rotate_counterclockwise)
            elif 'release' in move:
                result.append(self.__ctr.drop)
            else:
                errors.append(move)
        if errors:
            logging.warning(f'There are {len(errors)} AI response parsing errors: {",".join([str(e) for e in errors])}')
        else:
            logging.info(f'AI response parsing done successfully, there are {len(result)} moves scheduled in flight.')
        return result

    def get_flight_execution_interval_ms(self) -> int:
        return self.__flight_execution_interval_ms

    def build_flight(self, figure_rendering: FigureRendering, google_ai_api_key: str) -> None:
        logging.info(f'Build flight, calling Google AI with API key {google_ai_api_key[:5]}...')
        assert google_ai_api_key is not None
        well = figure_rendering.get_layout()
        well_text = '\n'.join([''.join(['1' if cell else '0' for cell in row]) for row in well])
        genai.configure(api_key=google_ai_api_key)
        response_text = self.__ask_ai(well_text)
        self.__flight_ops = self.__parse_ai_response(response_text)
        self.__current_fligh_op = 0
        logging.info(f'The flight build is completed. There are {len(self.__flight_ops)} moves.')

    def execute_flight(self) -> None:
        logging.info('Execute flight move')
        if self.__flight_ops:
            logging.info(f'Executing move {self.__current_fligh_op+1} of {len(self.__flight_ops)}')
            move_func = self.__flight_ops[self.__current_fligh_op]
            move_func()
            if self.__current_fligh_op < len(self.__flight_ops) - 1:
                self.__current_fligh_op += 1
            elif self.__current_fligh_op == len(self.__flight_ops) - 1:
                if move_func == self.__ctr.drop:
                    pass    # this is "release" - let it go down quickly
                else:
                    logging.warn(f'The last move in the sequence is not "release"')
                    self.__current_fligh_op = len(self.__flight_ops)
            else:
                # the flight is over
                pass
