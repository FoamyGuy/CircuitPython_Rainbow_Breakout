from displayio import Group
from vectorio import Circle
from .colors import palette


class Ball():
    def __init__(self, x=120, y=200, radius=4, color_index=0):
        self.shape = Circle(pixel_shader=palette, radius=radius, x=x, y=y)
        self.shape.color_index = 1
        self.speed_x = 0
        self.speed_y = 0

    @property
    def left(self):
        return self.shape.x - self.shape.radius

    @property
    def top(self):
        return self.shape.y - self.shape.radius

    @property
    def right(self):
        return self.shape.x + self.shape.radius

    @property
    def bottom(self):
        return self.shape.y + self.shape.radius

    def tick(self, game):
        self.shape.x += self.speed_x
        self.shape.y += self.speed_y

        if self.right >= game.display_size[0]:
            self.speed_x *= -1
        if self.left <= 0:
            self.speed_x *= -1

        if self.bottom >= game.display_size[1]:
            self.speed_y *= -1
        if self.top <= 0:
            self.speed_y *= -1


    @property
    def radius(self):
        return self.shape.radius

    @radius.setter
    def radius(self, new_val):
        self.shape.radius = new_val

    @property
    def x(self):
        return self.shape.x

    @x.setter
    def x(self, new_val):
        self.shape.x = new_val

    @property
    def y(self):
        return self.shape.y

    @y.setter
    def y(self, new_val):
        self.shape.y = new_val

