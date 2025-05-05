import math

class GameObject:
    # 建構式
    def __init__(self, playground=None):
        if playground is None:
            self._playground = [1200, 900]
        else:
            self._playground = playground

        # 移動範圍（左、右、上、下）
        self._objectBound = (0, self._playground[0], 0, self._playground[1])
        self._changeX = 0  # 座標改變變量
        self._changeY = 0
        self._x = 0        # 貼圖位置
        self._y = 0
        self._moveScale = 1  # 移動計量值
        self._hp = 1       # HP
        self._image = None
        self._available = True  # 有效物件
        self._center = None
        self._radius = None  # 碰撞半徑
        self._collided = False  # 是否產生碰撞

    # Python提供的getter
    @property
    def x(self):
        return self._x

    # Python提供的setter
    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def image(self):
        return self._image

    @property
    def xy(self):
        return (self._x, self._y)


    def to_the_left(self):
        self._changeX = -self._moveScale

    def to_the_right(self):
        self._changeX = self._moveScale

    def to_the_bottom(self):
        self._changeY = self._moveScale

    def to_the_top(self):
        self._changeY = -self._moveScale

    def stop_x(self):
        self._changeX = 0

    def stop_y(self):
        self._changeY = 0

    def update(self):
        self.x += self._changeX
        self.y += self._changeY

        if self.x > self._objectBound[1]:
            self.x = self._objectBound[1]
        if self.x < self._objectBound[0]:
            self.x = self._objectBound[0]
        if self.y > self._objectBound[3]:
            self.y = self._objectBound[3]
        if self.y < self._objectBound[2]:
            self.y = self._objectBound[2]

    def _collided_(self, it):
        distance = math.hypot(
            self._center[0] - it.center[0],
            self._center[1] - it.center[1]
        )
        if distance < self._radius + it.radius:
            return True
        else:
            return False
