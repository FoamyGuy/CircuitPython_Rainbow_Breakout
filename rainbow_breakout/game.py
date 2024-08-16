import terminalio
from displayio import Group
from rainbow_breakout.ball import Ball
from rainbow_breakout.paddle import Paddle
from rainbow_breakout.brick import Brick
from adafruit_display_text.bitmap_label import Label
from game_controls import game_controls

class Game(Group):
    TOP_PADDING = 10
    LEFT_PADDING = 10

    STATE_WAITING_TO_START = 0
    STATE_PLAYING = 1
    STATE_PAUSED = 2
    STATE_GAME_OVER = 3


    def __init__(self, display_size):
        super().__init__()
        self.display_size = display_size
        self.game_controls = game_controls
        self.balls = []
        self.bricks = []
        self.state = Game.STATE_WAITING_TO_START
        self._lives = 3
        self._score = 0
        self.balls.append(Ball())


        self.paddle = Paddle()

        self.lives_label = Label(terminalio.FONT, text=str(self._lives))
        self.lives_label.anchor_point = (0, 0)
        self.lives_label.anchored_position = (1, 1)
        self.append(self.lives_label)

        self.score_label = Label(terminalio.FONT, text=str(0))
        self.score_label.anchor_point = (1.0, 0)
        self.score_label.anchored_position = (display_size[0]-1, 1)
        self.append(self.score_label)

        for row in range(7):
            for col in range(10):
                self.bricks.append(Brick(x=col*20 + (2 * (col + 1)) + self.LEFT_PADDING,
                                         y=row * 9 + (2 * (row + 1)) + self.TOP_PADDING,
                                         color_index=row))
                # if self.bricks:
                #     self.bricks.append(Brick(x=self.bricks[-1].right + 2, y=row*9 + (2 * (row+1))))
                # else:
                #     self.bricks.append(Brick(x=2, y=2))
                self.append(self.bricks[-1].shape)
        self.append(self.paddle.shape)
        self.append(self.balls[0].shape)


    def tick(self):

        if self.state == Game.STATE_PLAYING:
            for ball in self.balls:
                ball.tick(self)
            self.paddle.tick(self)
            for brick in self.bricks:
                collided = brick.tick(self)
                if collided:
                    break
        if self.state == Game.STATE_WAITING_TO_START:
            cur_state = self.game_controls.button
            if cur_state["b"]:
                self.state = Game.STATE_PLAYING
                self.balls[0].speed_x = 1
                self.balls[0].speed_y = -1

        if self.state == Game.STATE_PAUSED:
            cur_state = self.game_controls.button
            if cur_state["b"]:
                self.state = Game.STATE_PLAYING


    @property
    def lives(self):
        return self._lives

    @lives.setter
    def lives(self, new_value):
        self._lives = new_value
        self.lives_label.text = str(self._lives)


    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, new_value):
        print("inside score setter")
        self._score = new_value
        self.score_label.text = str(self._score)
