import sys, logging
import tkinter as tk

from model import Board, Game
from view import CellRenderer, BoardRenderer
from controller import Controller

class App(object):
    def __init__(self, root: tk.Tk) -> None:
        super().__init__()
        self.root = root
        self.__init_ui()
        self.__init_mvc()

    def __init_ui(self) -> None:
        self.__win_width = BoardRenderer.CANVAS_WIDTH + 200
        self.__win_height = BoardRenderer.CANVAS_HEIGHT
        self.__gameframe_width = BoardRenderer.CANVAS_WIDTH
        self.__gameframe_height = self.__win_height

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

        self.scorevar = tk.IntVar()
        self.scorevar.set(0)
        self.scorelabel = tk.Label(self.controlframe, pady=10)
        self.scorelabel.grid(column=0, row=0)
        self.scorelabel["textvariable"] = self.scorevar
        
        self.startbutton = tk.Button(self.controlframe, text='Start / Restart')
        self.startbutton.grid(column=0, row = 1, pady=10)
        self.stopbutton = tk.Button(self.controlframe, text='Pause')
        self.stopbutton.grid(column=0, row = 2)
        
        self.mainframe.pack()
        logging.info('Init UI components - done.')

    def __push_down_timer(self):
        self.__ctr.push_down()
        self.root.after(self.__ctr.get_push_down_interval_ms(), self.__push_down_timer)

    def __update_score(self, score: int) -> None:
        self.scorevar.set(score)

    def __init_mvc(self) -> None:
        logging.info('Init MVC components...')
        
        # Model
        game = Game(self.__update_score)
        board = Board()

        # View
        figure_renderer = CellRenderer(self.canvas)
        board_renderer = BoardRenderer(self.canvas)

        # Controller
        self.__ctr = Controller(game, board, figure_renderer, board_renderer, self.__update_score)
        self.root.bind("<Right>", lambda event: self.__ctr.move_right())
        self.root.bind("<Left>", lambda event: self.__ctr.move_left())
        self.root.bind("<Up>", lambda event: self.__ctr.rotate_clockwise())
        self.root.bind("<Down>", lambda event: self.__ctr.rotate_counterclockwise())
        self.root.bind("<space>", lambda event: self.__ctr.drop())
        self.__ctr.start_game()

        self.root.after(self.__ctr.get_push_down_interval_ms(), self.__push_down_timer)
        logging.info('Init MVC components - done.')

    def run(self):
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
