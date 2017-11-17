import tkinter
import threading
import time
import random
import socket
import units
from controllib.system import Wait

print('ui.py start')


class GameBoard(threading.Thread):
    def __init__(self, root):
        print('GameBoard.__init__')
        self._unitDied = None  # Callback for when a player dies.
        self._canvas = None
        self._root = root

        lblIP = tkinter.Label(root, text='Game Server:  {} :{}'.format(
            socket.gethostbyname(socket.gethostname()),
            '3888',
        ))
        lblIP.grid(row=0, column=0, columnspan=2)


        self._width = 400
        self._height = 300

        self._createCanvas()

        self._units = set()
        self._bullets = set()
        self._gameOver = False

        self._NewPlayer = None #callback for when a new player (human or AI) is added to the game

        super().__init__()
        self.start()

        for i in range(1):
            self.AddAIUnit()
            pass

    def _createCanvas(self):
        print('GameBoard._createCanvas')
        self._canvas = tkinter.Canvas(self._root, width=self._width, height=self._height, background='grey')
        self._canvas.grid(row=1, column=1)

    def AddAIUnit(self):
        # TODO make this better
        randomPosition = self.GetRandomPosition()
        newColor = self.GetNewColor()
        newUnit = self.AddUnit(randomPosition[0], randomPosition[1], color=newColor)

        @Wait(0)
        def loop():
            while newUnit.isAlive:
                newUnit.Shoot(random.randint(0, 360))
                direction = random.choice(['Up', 'Down', 'Left', 'Right'])
                for i in range(random.randint(1, 100)):
                    newUnit.move(direction)
                    time.sleep(0.01)

    def AddUnit(self, x_center, y_center, color):
        newUnit = units.Unit(self, color, x_center, y_center)
        self._units.add(newUnit)

        if self.NewPlayer is not None:
            self.NewPlayer(self, newUnit)

        return newUnit

    def MoveUnit(self, unit, direction):
        #print('move_unit(unit={}, direction=())'.format(unit, direction))
        # direction is either a string like "Left", "Up" etc
        # or a float angle like 90 (90 degrees) 0 = right, 90 = up, 180 = left, 270 = down, -90 = down

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
        self.KeepUnitInBounds(unit)

    def GetAllUnits(self):
        return list(self._units.copy()) + list(self._bullets.copy())

    def KeepUnitInBounds(self, unit):
        if unit.x - unit._width/2 < 0: #unit is too far left
            dx = 0 - unit.x + unit._width/2 + 2
        elif unit.x + unit._width/2 > self._width: #unit is too far right
            dx = self._width - unit.x - unit._width/2 - 1
        else:
            dx = 0

        if unit.y - unit._width/2  < 0: #unit is too far up
            dy = 0 - unit.y + unit._width/2 + 2
        elif unit.y + unit._width/2  > self._height: #unit is too far down
            dy = self._height - unit.y - unit._width/2 - 1
        else:
            dy = 0

        if dx is not 0 or dy is not 0:
            self.MoveXY(unit, dx, dy)

    def MoveXY(self, unit, dx, dy):
        print('Game.MoveXY(unit={}, dx={}, dy={})'.format(unit, dx, dy))
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

            # print('{} - GameBoard.run()'.format(time.asctime()))

            for bullet in self._bullets.copy():
                bullet.Move()

            for unit in self._units.copy():
                overlaps = self._canvas.find_overlapping(*tuple(unit.coords))
                if len(overlaps) > 1:
                    for bullet in self._bullets.copy():
                        if bullet._item_number in overlaps:
                            if bullet.parent is not unit:
                                unit.Damage(bullet.parent)

            time.sleep(0.01)  # using this to slow down loop for debugging, will comment out in final product

    # Properties *************************

    # Async event that executes when a player has been killed
    @property
    def UnitDied(self):
        return self._unitDied

    @UnitDied.setter
    def UnitDied(self, func):
        self._unitDied = func

    # Async event that executes when a new player joins the game
    @property
    def NewPlayer(self):
        return self._NewPlayer  # This function will be called when a new player is added

    @NewPlayer.setter
    def NewPlayer(self, func):
        self._NewPlayer = func

    def GetRandomPosition(self):
        x = random.randint(0 + self._width /4, self._width * 3/4)
        y = random.randint(0 + self._height /4, self._height * 3/4)
        return (x, y)

    def GetNewColor(self):
        availableColors = ['Red', 'Orange', 'Yellow', 'Green', 'Cyan', 'Blue', 'Purple']

        for unit in self._units:
            availableColors.remove(unit._color)

        if len(availableColors) > 0:
            return availableColors.pop(0)
        else:
            return None

    def RegisterBullet(self, bullet):
        print('Game.RegisterBullet(bullet={})'.format(bullet))
        self._bullets.add(bullet)

    def RemoveUnit(self, unit):
        print('RemoveUnit(unit={})'.format(unit))
        if unit in self._bullets.copy():
            self._bullets.remove(unit)

        if unit in self._units.copy():
            self._units.remove(unit)
            if self._unitDied is not None:
                self._unitDied(unit, unit._killedBy)

        self._canvas.delete(unit._item_number)


print('end ui.py')
