import math
from controllib.system import Wait
import time

class Unit:
    #anything that appears on the playing field
    def __init__(self, game, color, x_center, y_center, width=10):
        self._game = game

        self._color = color
        self._width = width
        self._speed = 10
        self._defense_power = 10 #None = indestructable
        self._attack_power = 10
        self._shoot_range = 10
        self._item_number = None

        self._maxShootRate = 0.5 # bullets per second
        self._lastShootTime = 0

        self._put_unit_on_board(x_center, y_center)
        self._killedBy = None
        self._type = 'Unit'


    def _put_unit_on_board(self, x_center, y_center):
        x0 = x_center - self._width/2
        x1 = x_center + self._width/2
        y0 = y_center - self._width/2
        y1 = y_center + self._width/2

        self._item_number = self._game._canvas.create_oval(x0, y0, x1, y1, fill=self._color)

    def move(self, direction):
        self._game.move_unit(self, direction)

    def Shoot(self, direction):
        nowTime = time.time()

        if nowTime - self._lastShootTime > 1/self._maxShootRate:
            print('Unit.Shoot(direction={})'.format(direction))
            bullet = Bullet(self, direction)
            self._lastShootTime = nowTime


    @property
    def x(self):
        coords = self._game._canvas.coords(self._item_number)
        if len(coords) is 4:
            return (coords[2] + coords[0]) / 2
        else:
            return 0

    @property
    def y(self):
        coords = self._game._canvas.coords(self._item_number)
        if len(coords) is 4:
            return (coords[3] + coords[1]) / 2
        else:
            return 0

    @property
    def coords(self):
        return self._game._canvas.coords(self._item_number)

    def Damage(self, byUnit):
        self.Destroy(byUnit) # For now, one hit will result in death

    def Destroy(self, byUnit=None):
        self._killedBy = byUnit
        self._game.RemoveUnit(self)

    @property
    def color(self):
        return self._color

    @property
    def isAlive(self):
        if self._killedBy is None:
            return True
        else:
            return False

    @property
    def Type(self):
        return self._type


class Bullet(Unit):
    def __init__(self, parentUnit, direction):
        direction = float(direction)
        print('Bullet.__init__(parentUnit={}, direction={})'.format(parentUnit, direction))
        super().__init__(game=parentUnit._game, color='Black', x_center=parentUnit.x, y_center=parentUnit.y, width=5)
        self._direction = direction
        self._game.RegisterBullet(self)
        self._parentUnit = parentUnit

        self._dx = math.cos(math.radians(self.direction))
        self._dy = 0 - math.sin(math.radians(self.direction))

        self._type = 'Bullet'

    def Move(self):
        self._game._canvas.move(self._item_number, self._dx, self._dy)

        if not (0-self._width)/2 <= self.x <= self._game._width:
            self.Destroy()
        elif not (0-self._width)/2 <= self.y <= self._game._height:
            self.Destroy()

    @property
    def direction(self):
        return self._direction #Returned in degrees 0 = right, 90 = up, 180 = left, 270 = down

    @property
    def parent(self):
        return self._parentUnit

class Player(Unit):
    pass