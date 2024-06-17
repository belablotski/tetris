import os, sys, logging
import tkinter as tk
from tkinter import simpledialog, messagebox

from model import Game
from view import BoardView
from controller import Controller

class App(object):
    def __init__(self, root: tk.Tk) -> None:
        super().__init__()
        self.__board_rows = 25
        self.__board_cols = 12
        self.__cell_size_px = 30
        self.__root = root
        self.__game_paused = False
        self.__game_over = False
        self.__copilot_is_active = False
        self.__google_ai_api_key = None
        self.__google_ai_api_key_env_var = 'GOOGLE_AI_APIKEY'
        self.__init_ai()
        self.__init_ui()
        self.__init_mvc()

    def __init_ai(self) -> None:
        logging.info(f'Reading Google AI API key from {self.__google_ai_api_key_env_var} environment variable...')
        if self.__google_ai_api_key_env_var in os.environ:
            self.__google_ai_api_key = os.environ[self.__google_ai_api_key_env_var]
            logging.info(f'Google AI API key read successfully')
        else:
            logging.warning(f'Google AI API key can not be read from {self.__google_ai_api_key_env_var} - not a critical error, but AI co-pilot will not work.')

    def __init_ui(self) -> None:
        self.__gameframe_width = self.__board_cols * self.__cell_size_px
        self.__gameframe_height = self.__board_rows * self.__cell_size_px
        self.__win_width = self.__gameframe_width + 200
        self.__win_height = self.__gameframe_height

        logging.info('Init UI components...')
        self.__root.title('Tetris 0.1')
        self.__root.geometry(f'{self.__win_width}x{self.__win_height}')
        self.__mainframe = tk.Frame(self.__root, width=self.__win_width, height=self.__win_height)
        self.__gameframe = tk.Frame(self.__mainframe, background='yellow', width=self.__gameframe_width,
                                    height=self.__win_height)
        self.__gameframe.grid(column=0, row=0)
        self.__controlframe = tk.Frame(self.__mainframe, width=self.__win_width-self.__gameframe_width,
                                       height=self.__win_height, padx=20)
        self.__controlframe.grid(column=1, row=0)
        self.__canvas = tk.Canvas(self.__gameframe, width=self.__gameframe_width, height=self.__gameframe_height,
                                  background='lightblue')
        self.__canvas.pack()

        self.__scorelabelcapt = tk.Label(self.__controlframe, text='Score', pady=0)
        self.__scorelabelcapt.grid(column=0, row=0)
        self.__scorevar = tk.IntVar()
        self.__scorevar.set(0)
        self.__scorelabel = tk.Label(self.__controlframe, pady=10)
        self.__scorelabel.grid(column=0, row=1)
        self.__scorelabel["textvariable"] = self.__scorevar

        self.__scorelabelcapt = tk.Label(self.__controlframe, text='Lines', pady=0)
        self.__scorelabelcapt.grid(column=0, row=2)
        self.__linesvar = tk.IntVar()
        self.__linesvar.set(0)
        self.__lineslabel = tk.Label(self.__controlframe, pady=10)
        self.__lineslabel.grid(column=0, row=3)
        self.__lineslabel["textvariable"] = self.__linesvar
        
        self.__copilotbutton = tk.Button(self.__controlframe, text='AI co-pilot', command=self.__toggle_copilot)
        self.__copilotbutton.grid(column=0, row = 4, pady=10)
        self.__pausebutton = tk.Button(self.__controlframe, text='Pause', command=self.__toggle_pause)
        self.__pausebutton.grid(column=0, row = 5, pady=10)
        self.__restartbutton = tk.Button(self.__controlframe, text='Restart', command=self.__restart)
        self.__restartbutton.grid(column=0, row = 6, pady=10)
        
        self.__mainframe.pack()
        logging.info('Init UI components - done.')

    def __push_down_timer(self) -> None:
        self.__pausable(self.__ctr.push_down)
        self.__root.after(self.__ctr.get_push_down_interval_ms(), self.__push_down_timer)

    def __toggle_copilot(self) -> None:
        self.__copilot_is_active = not self.__copilot_is_active
        logging.info(f'AI Co-pilot status is {"on" if self.__copilot_is_active else "off"}')
        try:
            if self.__copilot_is_active and self.__google_ai_api_key is None:
                self.__pause(True)
                try:
                    ### TODO: remove
                    messagebox.showinfo('Tetris AI Co-pilot', 'Sorry, this is not fully implemented yet... Please check README.md for the details.')
                    self.__copilot_is_active = False
                    return
                    ###
                    answer = simpledialog.askstring('Tetris AI Co-pilot', 
                        f'The Google AI API key is not set in enviroment variable {self.__google_ai_api_key_env_var}. Please enter it here:')
                    logging.debug(f'Asking for Google API key, answer = {answer}')
                    if answer:
                        self.__google_ai_api_key = answer
                    else:
                        messagebox.showinfo('Tetris AI Co-pilot', 'Sorry, can not turn on AI co-pilot without Google AI API key. Please check README.md for the details.')
                        self.__copilot_is_active = False
                finally:
                    self.__pause(False)
        finally:
            self.__copilotbutton.config(relief="sunken" if self.__copilot_is_active else "raised")

    def __toggle_pause(self) -> None:
        self.__game_paused = not self.__game_paused
        logging.info(f'Pause the game {self.__game_paused}')
        self.__pausebutton.config(relief="sunken" if self.__game_paused else "raised")

    def __pause(self, pause: bool) -> None:
        if pause != self.__game_paused:
            self.__toggle_pause()

    def __restart(self) -> None:
        self.__game_over = False
        self.__ctr.reset()

    def __pausable(self, func):
        if self.__game_paused or self.__game_over:
            logging.debug(f'Game {"paused" if self.__game_paused else "over"}')
        else:
            return func()

    def __set_game_over(self) -> None:
        self.__game_over = True

    def __init_mvc(self) -> None:
        logging.info('Init MVC components...')
        
        # Model
        game = Game(rows=self.__board_rows, cols=self.__board_cols,
                    score_update_callback=lambda score: self.__scorevar.set(score), 
                    lines_update_callback=lambda lines: self.__linesvar.set(lines))

        # View
        board_view = BoardView(game.get_board(), self.__canvas, self.__cell_size_px)

        # Controller
        self.__ctr = Controller(game, board_view, self.__set_game_over)
        self.__root.bind("<Right>", lambda event: self.__pausable(self.__ctr.move_right))
        self.__root.bind("<Left>", lambda event: self.__pausable(self.__ctr.move_left))
        self.__root.bind("<Up>", lambda event: self.__pausable(self.__ctr.rotate_clockwise))
        self.__root.bind("<Down>", lambda event: self.__pausable(self.__ctr.rotate_counterclockwise))
        self.__root.bind("<space>", lambda event: self.__pausable(self.__ctr.drop))
        self.__ctr.start_game()

        self.__root.after(self.__ctr.get_push_down_interval_ms(), self.__push_down_timer)
        logging.info('Init MVC components - done.')

    def run(self) -> None:
        logging.info('Entering mainloop...')
        self.__root.mainloop()
        logging.info('Exiting mainloop.')

if __name__ == "__main__":
    loghandler = logging.StreamHandler(sys.stdout)
    loghandler.setFormatter(logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s"))
    logging.getLogger().addHandler(loghandler)
    logging.getLogger().setLevel(logging.DEBUG)
    
    logging.info('Starting Tk app...')

    win = tk.Tk()
    app = App(win)
    app.run()
    
    logging.info('Goodbye!')
