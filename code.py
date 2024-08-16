import time

import board
from rainbow_breakout.game import Game
from displayio import Group

FPS_TARGET = 60
FPS_DELAY = 1.0 / FPS_TARGET
FPS_DELAY_MS = 1000 // FPS_TARGET

display = board.DISPLAY


game = Game((display.width, display.height))

display.root_group = game

last_tick = time.monotonic()
while True:
    now = time.monotonic()
    #print(f"{last_tick} + {FPS_DELAY_MS} <= {now}")
    if last_tick + FPS_DELAY <= now:
        game.tick()
        last_tick = now

    #time.sleep(FPS_DELAY)
