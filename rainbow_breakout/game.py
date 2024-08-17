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


    def _init_bricks(self):
        for i in range(len(self.bricks) - 1, -1, -1):
            self.game_group.remove(self.bricks[i].shape)
            self.bricks.pop(i)

        for row in range(7):
            for col in range(10):
                self.bricks.append(Brick(x=col * 20 + (2 * (col + 1)) + self.LEFT_PADDING,
                                         y=row * 9 + (2 * (row + 1)) + self.TOP_PADDING,
                                         color_index=row))
                # if self.bricks:
                #     self.bricks.append(Brick(x=self.bricks[-1].right + 2, y=row*9 + (2 * (row+1))))
                # else:
                #     self.bricks.append(Brick(x=2, y=2))
                self.game_group.append(self.bricks[-1].shape)

    def reset(self):
        self._lives = 2
        self._score = 0
        self.lives_label.text = str(self.lives)
        self.score_label.text = str(self.score)
        while len(self.balls) > 1:
            self.balls.pop()

        self.balls[0].x = 120
        self.balls[0].y = 200
        self.paddle.x = 105
        self.paddle.y = 233

        self._init_bricks()

    def __init__(self, display_size):
        super().__init__()
        self.display_size = display_size
        self.game_controls = game_controls
        self.balls = []
        self.bricks = []
        self.state = Game.STATE_WAITING_TO_START
        self._lives = 2
        self._score = 0
        self.balls.append(Ball())

        self.game_group = Group()
        self.append(self.game_group)

        self.game_over_group = Group()
        self.game_over_label = Label(terminalio.FONT, text="GAME\nOVER", scale=3)
        self.game_over_label.anchor_point = (0.5, 0.5)
        self.game_over_label.anchored_position = (display_size[0] // 2, display_size[1] // 2)
        self.game_over_group.append(self.game_over_label)

        self.paddle = Paddle()

        self.lives_label = Label(terminalio.FONT, text=str(self._lives))
        self.lives_label.anchor_point = (0, 0)
        self.lives_label.anchored_position = (1, 1)
        self.game_group.append(self.lives_label)

        self.score_label = Label(terminalio.FONT, text=str(0))
        self.score_label.anchor_point = (1.0, 0)
        self.score_label.anchored_position = (display_size[0] - 1, 1)
        self.game_group.append(self.score_label)

        self._init_bricks()

        self.game_group.append(self.paddle.shape)
        self.game_group.append(self.balls[0].shape)

        self.prev_button_state = self.game_controls.button

    def tick(self):
        cur_button_state = self.game_controls.button
        if self.state == Game.STATE_PLAYING:
            for ball in self.balls:
                ball.tick(self)
            self.paddle.tick(self)
            for brick in self.bricks:
                collided = brick.tick(self)
                if collided:
                    break
        if self.state == Game.STATE_WAITING_TO_START:
            # print(f"cur btn state {cur_button_state}")
            # print(f"prev btn state {self.prev_button_state}")
            self.paddle.tick(self)
            if cur_button_state["b"] and not self.prev_button_state['b']:
                self.state = Game.STATE_PLAYING
                self.balls[0].speed_ratio = list(Ball.INITIAL_SPEED_RATIO)
                if self.paddle.recently_moving_direction == Paddle.DIRECTION_LEFT:
                    self.balls[0].speed_ratio[1] *= -1
                elif self.paddle.recently_moving_direction is None:
                    # randomly choose left or right
                    pass

                self.balls[0].speed_x = self.balls[0].speed_ratio[1]
                self.balls[0].speed_y = self.balls[0].speed_ratio[0]

        if self.state == Game.STATE_PAUSED:
            if cur_button_state["b"] and not self.prev_button_state['b']:
                self.state = Game.STATE_PLAYING

        if self.state == Game.STATE_GAME_OVER:
            if cur_button_state["b"] and not self.prev_button_state['b']:
                self.state = Game.STATE_WAITING_TO_START
                self.reset()
                self.remove(self.game_over_group)


        self.prev_button_state = dict(cur_button_state)
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
