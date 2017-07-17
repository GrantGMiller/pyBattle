class Unit:
    #anything that appears on the playing field
    def __init__(self, game, color, x_center, y_center):
        self._game = game

        self._color = color
        self._width = 10
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

class Bullet(Unit):
    def __init__(self):
        super().__init__()
        self._width = 1

class Player(Unit):
    pass