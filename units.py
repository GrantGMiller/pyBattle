class Unit:
    def __init__(self):
        self._width = 10
        self._speed = 10
        self._can_shoot = False
        self._defense_power = 10
        self._attack_power = 10
        self._shoot_range = 10

class Bullet(Unit):
    pass

class Player(Unit):
    pass