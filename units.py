class Unit:
    #anything that appears on the playing field
    def __init__(self, game, color, x_center, y_center, width=10):
        self._game = game

        self._color = color
        self._width = width
        self._speed = 10
        self._can_shoot = False
        self._defense_power = 10 #None = indestructable
        self._attack_power = 10
        self._shoot_range = 10
        self._item_number = None

        self._put_unit_on_board(x_center, y_center)

    def _put_unit_on_board(self, x_center, y_center):
        x0 = x_center - self._width/2
        x1 = x_center + self._width/2
        y0 = y_center - self._width/2
        y1 = y_center + self._width/2

        self._item_number = self._game._canvas.create_oval(x0, y0, x1, y1, fill=self._color)

    def move(self, direction):
        self._game.move_unit(self, direction)

    def Shoot(self, direction):
        print('Unit.Shoot(direction={})'.format(direction))
        bullet = Bullet(self, direction)

    @property
    def x(self):
        coords = self._game._canvas.coords(self._item_number)
        return (coords[2] + coords[0]) / 2

    @property
    def y(self):
        coords = self._game._canvas.coords(self._item_number)
        return (coords[3] + coords[1]) / 2

class Bullet(Unit):
    def __init__(self, parentUnit, direction):
        direction = float(direction)
        print('Bullet.__init__(parentUnit={}, direction={})'.format(parentUnit, direction))
        super().__init__(game=parentUnit._game, color='Black', x_center=parentUnit.x, y_center=parentUnit.y, width=5)
        self._direction = direction
        self._game.RegisterBullet(self)

    def MoveXY(self, dx, dy):
        print('Bullet.moveXY(dx={}, dy={})'.format(dx, dy))
        self._game._canvas.move(self._item_number, dx, dy)

        if not (0-self._width)/2 <= self.x <= self._game._width:
            self.Destroy()
        elif not (0-self._width)/2 <= self.y <= self._game._height:
            self.Destroy()

    def Destroy(self):
        print('Bullet.Destroy()')
        self._game.RemoveBullet(self)

    @property
    def direction(self):
        return self._direction


class Player(Unit):
    pass