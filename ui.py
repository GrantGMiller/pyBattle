import tkinter
import threading
import time
import random
import socket
import math

import units

print('ui.py start')


class GameBoard(threading.Thread):
    def __init__(self, root):
        print('GameBoard.__init__')
        self._player_died = None # Callback for when a player dies.
        self._canvas = None
        self._root = root

        lblIP = tkinter.Label(root, text='Game Server: ' + socket.gethostbyname(socket.gethostname()))
        lblIP.grid(row=0, column=0, columnspan=2)

        self._lblPlayers = tkinter.Label(root, text='Players:')
        self._lblPlayers.grid(row=1, column=0, sticky=tkinter.N + tkinter.W)

        self._width = 400
        self._height = 300

        self._createCanvas()

        self._units = set()
        self._bullets = set()
        self._gameOver = False

        super().__init__()
        self.start()

    def _createCanvas(self):
        print('GameBoard._createCanvas')
        self._canvas = tkinter.Canvas(self._root, width=self._width, height=self._height, background='grey')
        self._canvas.grid(row=1, column=1)


    def add_unit(self, x_center, y_center, color):
        newUnit = units.Unit(self, color, x_center, y_center)
        self._units.add(newUnit)
        return newUnit

    def move_unit(self, unit, direction):
        print('move_unit(unit={}, direction=())'.format(unit, direction))
        #direction is either a string like "Left", "Up" etc
        #or a float angle like 90 (90 degrees) 0 = right, 90 = up, 180 = left, 270 = down, -90 = down

        direction = direction.upper()
        dx = 0
        dy = 0
        if direction == 'UP':
            dy = -1
        elif direction == 'DOWN':
            dy = 1
        elif direction == 'LEFT':
            dx = -1
        elif direction == 'RIGHT':
            dx = 1

        self._canvas.move(unit._item_number, dx, dy)


    def GameOver(self):
        self._gameOver = True

    def run(self):
        '''
        This while-loop will check for actions like if a new char should be added, if a char should die, move units like bullets one step forward,
            commands from the user to move their troops.
        :return:
        '''
        while not self._gameOver:

            print('{} - GameBoard.run()'.format(time.asctime()))

            for bullet in self._bullets:
                dx = math.cos(math.radians(bullet.direction))
                dy = 0 - math.sin(math.radians(bullet.direction))
                print('dx={}, dy={}'.format(dx, dy))
                bullet.MoveXY(dx, dy)

            time.sleep(0.5) #using this to slow down loop for debugging, will comment out in final product

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
        return self._new_player #This function will be called when a new player is added

    @new_player.setter
    def new_player(self, func):
        self._new_player = func

    def GetRandomPosition(self):
        x = random.randint(0, self._width)
        y = random.randint(0, self._height)
        return (x, y)

    def GetNewColor(self):
        availableColors = ['Red', 'Orange', 'Yellow', 'Green', 'Blue', 'Purple']

        for unit in self._units:
            availableColors.remove(unit._color)

        if len(availableColors) > 0:
            return availableColors.pop(0)
        else:
            return None

    def RegisterBullet(self, bullet):
        print('Game.RegisterBullet(bullet={})'.format(bullet))
        self._bullets.add(bullet)

    def RemoveBullet(self, bullet):
        self._bullets.remove(bullet)

print('end ui.py')