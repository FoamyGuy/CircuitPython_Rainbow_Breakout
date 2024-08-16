import math

from vectorio import Rectangle
from .colors import palette
from game_controls import game_controls


class Brick:
    SIDE_LEFT = 0
    SIDE_TOP = 1
    SIDE_RIGHT = 2
    SIDE_BOTTOM = 3

    def __init__(self, x=0, y=0, width=20, height=9, color_index=0):
        self.shape = Rectangle(pixel_shader=palette, width=width, height=height, x=x, y=y)
        self.shape.color_index = color_index

    def tick(self, game):
        for ball in game.balls:
            # if ball is colliding
            colliding = self.is_colliding(ball)
            if colliding[0]:
                print(f"ball is colliding side is: {colliding[1]}")
                if colliding[1] in (Brick.SIDE_LEFT, Brick.SIDE_RIGHT):
                    ball.speed_x *= -1
                    game.bricks.remove(self)
                    game.remove(self.shape)
                    if self.shape.color_index == ball.shape.color_index:
                        game.score += 25
                    else:
                        game.score += 5
                    return True
                elif colliding[1] in (Brick.SIDE_TOP, Brick.SIDE_BOTTOM):
                    ball.speed_y *= -1
                    game.bricks.remove(self)
                    game.remove(self.shape)
                    if self.shape.color_index == ball.shape.color_index:
                        game.score += 25
                    else:
                        game.score += 5
                    return True
        return False


    def is_colliding(self, ball):
        cx, cy = ball.x, ball.y

        # if self.left - ball.radius <= cx <= self.right + ball.radius and \
        #         self.top - ball.radius <= cy <= self.bottom + ball.radius:

        if self.shape.intersects(ball.shape):

            # left edge
            if self.left - ball.radius <= cx <= self.left:
                if self.top - ball.radius <= cy <= self.top + ball.radius:
                    return (True, Brick.SIDE_LEFT)

            if self.right <= cx <= self.right + ball.radius:
                if self.top - ball.radius <= cy <= self.bottom + ball.radius:
                    return (True, Brick.SIDE_RIGHT)

            if self.top - ball.radius <= cy <= self.top:
                if self.left - ball.radius <= cx <= self.right + ball.radius:
                    return (True, Brick.SIDE_TOP)

            if self.bottom <= cy <= self.bottom + ball.radius:
                if self.left - ball.radius <= cx <= self.right + ball.radius:
                    return (True, Brick.SIDE_BOTTOM)

        return (False, None)

    """
    def is_colliding(self, ball):
        # def check_collision(cx, cy, radius, rect_left, rect_top, rect_right, rect_bottom):
        cx = ball.x
        cy = ball.y

        testX = cx
        testY = cy
        # print(f"cx: {cx}, cy: {cy} radius: {radius}")
        # print(f"rect_left: {rect_left}, rect_top: {rect_top}, rect_right: {rect_right}, rect_bottom: {rect_bottom}")
        closest_x = Brick.SIDE_LEFT
        closest_y = Brick.SIDE_BOTTOM
        if (cx < self.left):
            closest_x = Brick.SIDE_LEFT
            testX = self.left
        elif (cx > self.right):
            closest_x = Brick.SIDE_RIGHT
            testX = self.right

        if (cy < self.top):
            closest_y = Brick.SIDE_TOP
            testY = self.top
        elif (cy > self.bottom):
            closest_y = Brick.SIDE_BOTTOM
            testY = self.bottom

        # print(f"testX: {testX}, testY: {testY}")
        distX = cx - testX
        distY = cy - testY
        
        closest = closest_x if distX <= distY else closest_y
        # print(f"distX: {distX}, distY: {distY}")
        dist = math.sqrt(distX ** 2 + distY ** 2)
        # print(f"dist is: {dist}")
        if dist <= ball.radius:

            return (True, closest)
        return (False, None)
    """

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
