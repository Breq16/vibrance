import pygame
import sys

import vibrance
import vibrance.pygame_if

PALETTE = (
    "000000",  # black
    "FFFFFF",  # white
    "FF0000",  # red
    "00FF00",  # green
    "0000FF",  # blue
    "FFFF00",  # yellow
    "00FFFF",  # cyan
    "FF00FF",  # magenta
    "FF8000",  # orange
    "8000FF",  # purple
    "0080FF",  # light blue
    "FF0080",  # pink
)

color = "000000"

api = vibrance.pygame_if.PyGameInterface()

enabled = {zone: False for zone in range(6)}

def setEnabled(key, state):
    global enabled
    if key in (pygame.K_KP1, ord('1')):
        enabled[0] = state
        enabled[3] = state
    elif key in (pygame.K_KP2, ord('2')):
        enabled[1] = state
        enabled[4] = state
    elif key in (pygame.K_KP3, ord('3')):
        enabled[2] = state
        enabled[5] = state
    elif key in (pygame.K_KP4, ord('4')):
        enabled[3] = state
    elif key in (pygame.K_KP5, ord('5')):
        enabled[4] = state
    elif key in (pygame.K_KP6, ord('6')):
        enabled[5] = state
    elif key in (pygame.K_KP7, ord('7')):
        enabled[0] = state
    elif key in (pygame.K_KP8, ord('8')):
        enabled[1] = state
    elif key in (pygame.K_KP9, ord('9')):
        enabled[2] = state
    elif key in (pygame.K_KP0, ord('0')):
        enabled[0] = state
        enabled[1] = state
        enabled[2] = state
        enabled[3] = state
        enabled[4] = state
        enabled[5] = state


def changeColor(key):
    global color
    if key == ord('q'):
        color = PALETTE[0]
    elif key == ord('w'):
        color = PALETTE[1]
    elif key == ord('e'):
        color = PALETTE[2]
    elif key == ord('r'):
        color = PALETTE[3]
    elif key == ord('a'):
        color = PALETTE[4]
    elif key == ord('s'):
        color = PALETTE[5]
    elif key == ord('d'):
        color = PALETTE[6]
    elif key == ord('f'):
        color = PALETTE[7]
    elif key == ord('z'):
        color = PALETTE[8]
    elif key == ord('x'):
        color = PALETTE[9]
    elif key == ord('c'):
        color = PALETTE[10]
    elif key == ord('v'):
        color = PALETTE[11]

@api.keydown
def keydown(key, pygame_in):
    if ((ord('0') <= key <= ord('9'))
            or (pygame.K_KP0 <= key <= pygame.K_KP9)):
        setEnabled(key, True)
    else:
        changeColor(key)
    update(pygame_in)

@api.keyup
def keyup(key, pygame_in):
    setEnabled(key, False)
    update(pygame_in)

def update(pygame_in):
    global color
    for zone in enabled.keys():
        api.color(zone, color if enabled[zone] else "000")

    pygame_in.setColor(color)

if __name__ == "__main__":
    ctrl = vibrance.Controller()
    ctrl.connect(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)

    pygame_in = vibrance.pygame_if.PyGameInput()

    api.run(pygame_in, ctrl)
