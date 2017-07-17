import tkinter
import threading
import time

print('ui.py start')


class GameBoard(threading.Thread):
    def __init__(self, root):
        print('GameBoard.__init__')
        self._player_died = None
        self._canvas = None
        self._root = root

        self._createCanvas()

        super().__init__()
        self.start()

    def _createCanvas(self):
        print('GameBoard._createCanvas')
        self._canvas = tkinter.Canvas(self._root, width=400, height=300, background='grey')
        self._canvas.pack()
        self._add_unit()


    def _add_unit(self, x_center, y_center):
        width = 10
        x0 =
        self._canvas.create_oval(10,20,30,40, fill='blue')

    def run(self):
        while True:
            print('{} - GameBoard.run()'.format(time.asctime()))
            time.sleep(3)

    #Properties *************************

    #Async event that executes when a player has been killed
    @property
    def player_died(self):
        return self._player_died

    @player_died.setter
    def player_died(self, func):
        self._player_died = func

    #Async event that executes when a new player joins the game
    @property
    def new_player(self):
        return self._new_player

    @new_player.setter
    def new_player(self, func):
        self._new_player = func

print('end ui.py')