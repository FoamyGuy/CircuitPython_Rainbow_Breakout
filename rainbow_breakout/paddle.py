import math

from vectorio import Rectangle
from .colors import palette



class Paddle():

    SECTION_OUTSIDE = -1
    SECTION_LEFT = 0
    SECTION_MIDDLE = 1
    SECTION_RIGHT = 2

    DIRECTION_LEFT = 0
    DIRECTION_RIGHT = 1

    def __init__(self, x=105, y=233, width=30, height=6, color_index=0):
        self.shape = Rectangle(pixel_shader=palette, width=width, height=height, x=x, y=y)
        self.shape.color_index = color_index
        self.speed_x = 0
        self.speed = 2
        self.prev_state = None
        self.recently_moving_direction = None

    def tick(self, game):
        cur_state = game.game_controls.button
        #print(f"right: {self.right} <= {game.display_size[0]}: {self.right <= game.display_size[0]}")
        if cur_state['right']:
            self.recently_moving_direction = self.DIRECTION_RIGHT
            if self.right <= game.display_size[0]:
                self.speed_x = self.speed

            else:
                self.speed_x = 0

        if cur_state['left']:
            self.recently_moving_direction = self.DIRECTION_LEFT
            if self.left >= 0:
                self.speed_x = -self.speed
            else:
                self.speed_x = 0



        if not cur_state['right'] and not cur_state['left']:
            self.speed_x = 0

        self.shape.x += self.speed_x
        if game.state == game.STATE_WAITING_TO_START:
            game.balls[0].x = self.midpoint
        elif game.state == game.STATE_PLAYING:

            if cur_state['b'] and self.prev_state is not None and not self.prev_state['b']:
                print(f"b: {cur_state['b']} prev_b: {self.prev_state['b']}")

                self.shape.color_index = (self.shape.color_index + 1) % len(palette)

            for ball in game.balls:
                # if ball is colliding and moving downward
                if self.is_colliding(ball) and ball.speed_y > 0:
                    hit_section = self.ball_section(ball)
                    if hit_section == Paddle.SECTION_LEFT:
                        if ball.speed_x > 0:
                            ball.speed_ratio[1] += 1
                        else:
                            ball.speed_ratio[1] -= 1
                    elif hit_section == Paddle.SECTION_RIGHT:
                        if ball.speed_x > 0:
                            ball.speed_ratio[1] -= 1
                        else:
                            ball.speed_ratio[1] += 1

                    ball.speed_ratio[0] *= -1
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
    def midpoint(self):
        return self.x + self.width // 2

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

    def ball_section(self, ball):
        """
        return which of the 3 horizontal sections of the paddle the ball
        is within.
        :return:
        """

        one_third_point = self.x + self.width // 3
        two_third_point = self.x + (self.width // 3) * 2

        if self.x - ball.radius <= ball.x <= one_third_point:
            return self.SECTION_LEFT
        elif one_third_point <= ball.x <= two_third_point:
            return self.SECTION_MIDDLE
        elif two_third_point <= ball.x <= self.x + self.width + ball.radius:
            return self.SECTION_RIGHT
        else:
            return self.SECTION_OUTSIDE
