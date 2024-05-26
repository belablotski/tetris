import sys, logging
import tkinter as tk

class App(object):
    def __init__(self, root: tk.Tk) -> None:
        super().__init__()

        self.__win_width = 800
        self.__win_height = 800
        self.__gameframe_width = 600
        self.__gameframe_height = self.__win_height

        self.root = root
        self.root.title('Tetris 0.1')
        self.root.geometry(f'{self.__win_width}x{self.__win_height}')
        self.mainframe = tk.Frame(self.root, width=self.__win_width, height=self.__win_height)
        self.gameframe = tk.Frame(self.mainframe, background='yellow', width=self.__gameframe_width,
                                    height=self.__win_height)
        self.gameframe.grid(column=0, row=0)
        self.controlframe = tk.Frame(self.mainframe, background='green', width=self.__win_width-self.__gameframe_width,
                                    height=self.__win_height)
        self.controlframe.grid(column=1, row=0)
        self.canvas = tk.Canvas(self.gameframe, width=self.__gameframe_width, height=self.__gameframe_height,
                                    background='lightblue')
        self.canvas.pack()

        self.scorevar = tk.IntVar()
        self.scorevar.set(1000000)
        self.scorelabel = tk.Label(self.controlframe, pady=10)
        self.scorelabel.grid(column=0, row=0)
        self.scorelabel["textvariable"] = self.scorevar
        
        self.startbutton = tk.Button(self.controlframe, text='Start / Restart')
        self.startbutton.grid(column=0, row = 1, pady=10)
        self.stopbutton = tk.Button(self.controlframe, text='Pause')
        self.stopbutton.grid(column=0, row = 2)
        
        x = y = 50
        points = [x, y, x+20, y, x+20, y+20, x, y+20]
        self.canvas.create_polygon(points, outline='blue', fill='green', width=3)
        
        self.mainframe.pack()

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
    