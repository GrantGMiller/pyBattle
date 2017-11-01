import tkinter
import threading
import time

import units

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


    def add_unit(self, x_center, y_center, color):
        newUnit = units.Unit(self, color, x_center, y_center)
        return newUnit

    def move_unit(self, unit, direction):
        print('move_unit(unit={}, direction=())'.format(unit, direction))
        #direction is either a string like "Left", "Up" etc
        #or a float angle like 90 (90 degrees) 0 = right, 90 = up, 180 = left, 270 = down, -90 = down

        direction = direction.upper()
        dx = 0
        dy = 0
        if direction == 'Up':
            dy = -1
        elif direction == 'Down':
            dy = 1
        elif direction == 'Left':
            dx = -1
        elif direction == 'Right':
            dx = 1

        self._canvas.move(unit._item_number, dx, dy)

    def run(self):
        '''
        This while-loop will check for actions like if a new char should be added, if a char should die, move units like bullets one step forward,
            commands from the user to move their troops.
        :return:
        '''
        while True:

            print('{} - GameBoard.run()'.format(time.asctime()))
            time.sleep(3) #using this to slow down loop for debugging, will comment out in final product

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