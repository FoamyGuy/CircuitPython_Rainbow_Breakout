import math

from vectorio import Rectangle
from .colors import palette



class Paddle():
    def __init__(self, x=105, y=233, width=30, height=6, color_index=0):
        self.shape = Rectangle(pixel_shader=palette, width=width, height=height, x=x, y=y)
        self.shape.color_index = color_index
        self.speed_x = 0
        self.speed = 2
        self.prev_state = None

    def tick(self, game):
        cur_state = game.game_controls.button
        #print(f"right: {self.right} <= {game.display_size[0]}: {self.right <= game.display_size[0]}")
        if cur_state['right']:
            if self.right <= game.display_size[0]:
                self.speed_x = self.speed
            else:
                self.speed_x = 0

        if cur_state['left']:
            if self.left >= 0:
                self.speed_x = -self.speed
            else:
                self.speed_x = 0

        if cur_state['b'] and self.prev_state is not None and not self.prev_state['b']:
            print(f"b: {cur_state['b']} prev_b: {self.prev_state['b']}")

            self.shape.color_index = (self.shape.color_index + 1) % len(palette)

        if not cur_state['right'] and not cur_state['left']:
            self.speed_x = 0

        self.shape.x += self.speed_x

        for ball in game.balls:
            # if ball is colliding and moving downward
            if self.is_colliding(ball) and ball.speed_y > 0:
                ball.speed_y *= -1
                ball.shape.color_index = self.shape.color_index
        self.prev_state = dict(cur_state)

    def is_colliding(self, ball):
        # def check_collision(cx, cy, radius, rect_left, rect_top, rect_right, rect_bottom):
        cx = ball.x
        cy = ball.y

        testX = cx
        testY = cy
        # print(f"cx: {cx}, cy: {cy} radius: {radius}")
        # print(f"rect_left: {rect_left}, rect_top: {rect_top}, rect_right: {rect_right}, rect_bottom: {rect_bottom}")
        if (cx < self.left):
            testX = self.left
        elif (cx > self.right):
            testX = self.right

        if (cy < self.top):
            testY = self.top
        elif (cy > self.bottom):
            testY = self.bottom

        # print(f"testX: {testX}, testY: {testY}")
        distX = cx - testX
        distY = cy - testY

        # print(f"distX: {distX}, distY: {distY}")
        dist = math.sqrt(distX ** 2 + distY ** 2)
        # print(f"dist is: {dist}")
        if dist <= ball.radius:
            return True
        return False

    @property
    def left(self):
        return self.shape.x

    @property
    def top(self):
        return self.shape.y

    @property
    def right(self):
        return self.shape.x + self.shape.width

    @property
    def bottom(self):
        return self.shape.y + self.shape.height

    @property
    def width(self):
        return self.shape.width

    @width.setter
    def width(self, new_val):
        self.shape.width = new_val

    @property
    def height(self):
        return self.shape.height

    @height.setter
    def height(self, new_val):
        self.shape.height = new_val

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
