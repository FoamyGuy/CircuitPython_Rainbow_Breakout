from displayio import Group
from rainbow_breakout.ball import Ball
from rainbow_breakout.paddle import Paddle
from rainbow_breakout.brick import Brick


class Game(Group):
    def __init__(self, display_size):
        super().__init__()
        self.display_size = display_size
        self.balls = []
        self.bricks = []

        self.balls.append(Ball())
        self.balls[0].speed_x = 1
        self.balls[0].speed_y = -1

        self.paddle = Paddle()

        for row in range(7):
            for col in range(10):
                self.bricks.append(Brick(x=col*20 + (2 * (col + 1)),
                                         y=row * 9 + (2 * (row + 1)),
                                         color_index=row))
                # if self.bricks:
                #     self.bricks.append(Brick(x=self.bricks[-1].right + 2, y=row*9 + (2 * (row+1))))
                # else:
                #     self.bricks.append(Brick(x=2, y=2))
                self.append(self.bricks[-1].shape)
        self.append(self.paddle.shape)
        self.append(self.balls[0].shape)


    def tick(self):
        for ball in self.balls:
            ball.tick(self)
        self.paddle.tick(self)
        for brick in self.bricks:
            collided = brick.tick(self)
            if collided:
                break
