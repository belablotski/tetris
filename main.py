import sys, logging
import tkinter as tk

from model import Game
from view import BoardView
from controller import Controller

class App(object):
    def __init__(self, root: tk.Tk) -> None:
        super().__init__()
        self.__board_rows = 25
        self.__board_cols = 12
        self.__cell_size_px = 30
        self.root = root
        self.__game_paused = False
        self.__game_over = False
        self.__init_ui()
        self.__init_mvc()

    def __init_ui(self) -> None:
        self.__gameframe_width = self.__board_cols * self.__cell_size_px
        self.__gameframe_height = self.__board_rows * self.__cell_size_px
        self.__win_width = self.__gameframe_width + 200
        self.__win_height = self.__gameframe_height

        logging.info('Init UI components...')
        self.root.title('Tetris 0.1')
        self.root.geometry(f'{self.__win_width}x{self.__win_height}')
        self.mainframe = tk.Frame(self.root, width=self.__win_width, height=self.__win_height)
        self.gameframe = tk.Frame(self.mainframe, background='yellow', width=self.__gameframe_width,
                                    height=self.__win_height)
        self.gameframe.grid(column=0, row=0)
        self.controlframe = tk.Frame(self.mainframe, width=self.__win_width-self.__gameframe_width,
                                    height=self.__win_height, padx=20)
        self.controlframe.grid(column=1, row=0)
        self.canvas = tk.Canvas(self.gameframe, width=self.__gameframe_width, height=self.__gameframe_height,
                                    background='lightblue')
        self.canvas.pack()

        self.scorelabelcapt = tk.Label(self.controlframe, text='Score', pady=0)
        self.scorelabelcapt.grid(column=0, row=0)
        self.scorevar = tk.IntVar()
        self.scorevar.set(0)
        self.scorelabel = tk.Label(self.controlframe, pady=10)
        self.scorelabel.grid(column=0, row=1)
        self.scorelabel["textvariable"] = self.scorevar

        self.scorelabelcapt = tk.Label(self.controlframe, text='Lines', pady=0)
        self.scorelabelcapt.grid(column=0, row=2)
        self.linesvar = tk.IntVar()
        self.linesvar.set(0)
        self.lineslabel = tk.Label(self.controlframe, pady=10)
        self.lineslabel.grid(column=0, row=3)
        self.lineslabel["textvariable"] = self.linesvar
        
        self.pausebutton = tk.Button(self.controlframe, text='Pause', command=self.__pause)
        self.pausebutton.grid(column=0, row = 4, pady=10)
        self.restartbutton = tk.Button(self.controlframe, text='Restart', command=self.__restart)
        self.restartbutton.grid(column=0, row = 5)
        
        self.mainframe.pack()
        logging.info('Init UI components - done.')

    def __push_down_timer(self) -> None:
        self.__pausable(self.__ctr.push_down)
        self.root.after(self.__ctr.get_push_down_interval_ms(), self.__push_down_timer)

    def __pause(self) -> None:
        self.__game_paused = not self.__game_paused
        logging.info(f'Pause the game {self.__game_paused}')
        self.pausebutton.config(relief="sunken" if self.__game_paused else "raised")

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
                    score_update_callback=lambda score: self.scorevar.set(score), 
                    lines_update_callback=lambda lines: self.linesvar.set(lines))

        # View
        board_view = BoardView(game.get_board(), self.canvas, self.__cell_size_px)

        # Controller
        self.__ctr = Controller(game, board_view, self.__set_game_over)
        self.root.bind("<Right>", lambda event: self.__pausable(self.__ctr.move_right))
        self.root.bind("<Left>", lambda event: self.__pausable(self.__ctr.move_left))
        self.root.bind("<Up>", lambda event: self.__pausable(self.__ctr.rotate_clockwise))
        self.root.bind("<Down>", lambda event: self.__pausable(self.__ctr.rotate_counterclockwise))
        self.root.bind("<space>", lambda event: self.__pausable(self.__ctr.drop))
        self.__ctr.start_game()

        self.root.after(self.__ctr.get_push_down_interval_ms(), self.__push_down_timer)
        logging.info('Init MVC components - done.')

    def run(self) -> None:
        logging.info('Entering mainloop...')
        self.root.mainloop()
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
