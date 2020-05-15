import time

from . import *

PALETTE = (
    "000000", # black
    "FFFFFF", # white
    "FF0000", # red
    "00FF00", # green
    "0000FF", # blue
    "FFFF00", # yellow
    "00FFFF", # cyan
    "FF00FF", # magenta
    "FF8000", # orange
    "8000FF", # purple
    "0080FF", # light blue
    "FF0080", # pink
)

api = Interface("cloud.itsw.es")

@api.onOctave(0)
def cycle(msg):
    i = msg.note % 12

    api.fill((9001, 9004), PALETTE[i])
    api.fill((9002, 9003, 9005, 9006), "000")
    api.update()
    time.sleep(0.5)

    api.fill((9002, 9005), PALETTE[i])
    api.fill((9001, 9003, 9004, 9006), "000")
    api.update()
    time.sleep(0.5)

    api.fill((9003, 9006), PALETTE[i])
    api.fill((9001, 9002, 9004, 9005), "000")
    api.update()
    time.sleep(0.5)

    api.fill((9002, 9005), PALETTE[i])
    api.fill((9001, 9003, 9004, 9006), "000")
    api.update()

@api.onOctave(1)
def expand(msg):
    i = msg.note % 12

    api.add(9002, PALETTE[i])
    api.fill((9001, 9003, 9004, 9005, 9006), "000")
    api.update()
    time.sleep(0.5)

    api.fill((9001, 9003, 9005), PALETTE[i])
    api.fill((9002, 9004, 9006), "000")
    api.update()
    time.sleep(0.5)

    api.fill((9004, 9006), PALETTE[i])
    api.fill((9001, 9002, 9003, 9005), "000")
    api.update()


api.run()
