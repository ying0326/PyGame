from pathlib import Path
from typing import Union
import pygame
from gobject import GameObject
import math

class Player(GameObject):
    def __init__(self, playground, xy=None, sensitivity=1):
        GameObject.__init__(self, playground)
        self._moveScale = 1.0 * sensitivity
        __parent_path = Path(__file__).parents[1]
        self.__player_path = __parent_path / 'res' / 'airplan.png'
        self._image = pygame.image.load(self.__player_path)
        self._center = self._x + self._image.get_rect().w / 2, self._y + self._image.get_rect().h / 2
        self._radius = 0.3 * math.hypot(self._image.get_rect().w, self._image.get_rect().h)

        if xy is None:
            self._x = (self._playground[0] - self._image.get_rect().w) / 2
            self._y = 3 * self._playground[1] / 4
        else:
            self._x = xy[0]
            self._y = xy[1]

        # 左、右、上、下邊界限制
        self._objectBound = (
            10,
            self._playground[0] - (self._image.get_rect().w + 10),
            10,
            self._playground[1] - (self._image.get_rect().h + 10)
        )

    # 左移
    def to_the_left(self):
        self._x -= self._moveScale
        if self._x < self._objectBound[0]:
            self._x = self._objectBound[0]

    # 右移
    def to_the_right(self):
        self._x += self._moveScale
        if self._x > self._objectBound[1]:
            self._x = self._objectBound[1]

    # 上移
    def to_the_top(self):
        self._y -= self._moveScale
        if self._y < self._objectBound[2]:
            self._y = self._objectBound[2]

    # 下移
    def to_the_bottom(self):
        self._y += self._moveScale
        if self._y > self._objectBound[3]:
            self._y = self._objectBound[3]

    # 停止 X 軸移動
    def stop_x(self):
        self._changeX = 0

    # 停止 Y 軸移動
    def stop_y(self):
        self._changeY = 0

    def update(self):
        GameObject.update(self)
        self._center = self._x + self._image.get_rect().w / 2, self._y + self._image.get_rect().h / 2

    @property
    def image(self):
        return self._image

    @property
    def xy(self):
        return (self._x, self._y)
